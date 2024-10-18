from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps
import random
import smtplib
from flask import Blueprint, jsonify, request
from api import db
from .models import OTP, TOKEN


otpservice = Blueprint('otpservice', __name__)



# Define a decorator function to check for the token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing', "code":401})

        # Verify the token against your expected token
        gettoken = TOKEN.query.filter_by(id=1).first()
        auth_token = gettoken.tokenid
        if token != auth_token:
            return jsonify({'message': 'Invalid token', "code": 401})

        return f(*args, **kwargs)
    return decorated


@otpservice.route('/otp-sent', methods=['POST'])
def OTPsent(sender="ajaysharma713347@gmail.com",  custom_text="Hello, Your OTP is ", subject="OTP"):
    data = request.get_json() 
    email = data.get('email')
    
    
    if not email:
        return jsonify({"message": "Email parameters is required", "code": 400})
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = email
    msg['Subject'] = subject
    generatedOTP = generateOTP() 
    body = custom_text + generatedOTP
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    google_app_password = "foezjxdkfexcnbyi" 
    server.login(sender, google_app_password)
    server.sendmail(sender, email, msg.as_string())
    setData(generatedOTP, email )
    server.quit()
    
    return body

  
@otpservice.route('/otp-verify', methods=['POST'])
# @token_required
def OTPverify():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')
    
    if not email or not otp:
        return jsonify({"message": "Email and OTP parameters are required","code":400})
    
    existingData = OTP.query.filter_by(email=email).first()
    
    if existingData:
        if existingData.OTPcode == otp:
            # if(existingData.Isverify == 1):
                # existingData.Isverify = 1 change isVerfiy to 1
            db.session.commit()
            return jsonify({"message": "User's email is verified","code":200})
            # else:
            #     return jsonify({"message":'User is Already Verified', 'code': 409})
        else:
            return jsonify({"message": "Provided OTP is wrong", 'code':409})
    else:
        return jsonify({"message": "User not found with provided email", 'code':404})

def generateOTP(otp_size = 4):
    final_otp = ''
    for i in range(otp_size):
        final_otp = final_otp + str(random.randint(0,9))
    return final_otp


def setData(otpValue, email):
    exiting_User = OTP.query.filter_by(email=email).first()
    if exiting_User:
        print(exiting_User.OTPcode , otpValue)
        exiting_User.OTPcode = otpValue
        db.session.commit()
        print('OTP Updated!')
    else:
        otpData = OTP(OTPcode=otpValue, email=email, Isverify=0)
        print(otpData, otpValue)
        db.session.add(otpData)
        db.session.commit()
        print('OTP Added!')

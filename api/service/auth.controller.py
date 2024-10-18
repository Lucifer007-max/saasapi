from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
from sqlalchemy import or_
from api import db
from api.models import Users  # Import your model
import jwt
import datetime

authservice = Blueprint('authservice', __name__)

# Secret key for encoding JWT
SECRET_KEY = 'your_secret_key'

# Login API
@authservice.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from request
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password required'}), 400

    # Query the user from the database
    user = Users.query.filter_by(email=email).first()

    # Check if the user exists and the password is correct
    if user and check_password_hash(user.password, password):
        # Create JWT token
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, SECRET_KEY)

        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

# Helper function to decode the token (optional)
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    
    return decorated

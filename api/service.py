from flask import Blueprint, jsonify, request
from api import db
from api.models import Users  # Import your Users model
from werkzeug.security import generate_password_hash, check_password_hash
import io
# import os
import subprocess
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import PyPDF2

# Create Blueprint
service = Blueprint('service', __name__)

@service.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Get JSON data from the request
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = Users.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Verify password
    if user.password != password:
        return jsonify({'message': 'Invalid password'}), 401


    # Successful login response
    return jsonify({'message': 'Login successful', 'user_id': user.id}), 200




# Register Route
@service.route('/register', methods=['POST'])
def register():
    data = request.get_json()  # Get JSON data from the request
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user')  # Default role as 'user' if not provided

    # Check if user already exists
    if Users.query.filter_by(email=email).first():
        return jsonify({'message': 'User already exists'}), 409
    
    
    # Hashing the password before storing it
    # hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    # Hash the password
    # hashed_password =password

    # Create a new user instance
    new_user = Users(
        email=email,
        password=password,
        role=role,
        Isverify=0  # Default Isverify status, adjust as needed
    )

    # Add and commit new user to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201





@service.route('/pdf-path', methods=['POST'])
def pdfData():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    pdf_file = request.files['pdf_file']
    pdf_file_stream = io.BytesIO(pdf_file.read()) 
    print(pdf_file)
    ocr_output_stream = io.BytesIO()
    process = subprocess.run(
        ["ocrmypdf", "-", "-", "--output-type", "pdf", "--force-ocr"],
        input=pdf_file_stream.getvalue(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode != 0:
        return jsonify({'error': 'OCR processing failed', 'details': process.stderr.decode()}), 500
    
    ocr_output_stream.write(process.stdout)

    ocr_output_stream.seek(0)  
    pdf_reader = PyPDF2.PdfReader(ocr_output_stream)
    
    num_pages = len(pdf_reader.pages)
    text_data = {}
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        text_data[f"Page {page_num + 1}"] = text
        print(f"Text on page {page_num + 1}:\n{text}\n")
        return jsonify({'message': 'File uploaded successfully', 'text_data': text}), 200


    # SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), 'api', 'credentials.json')
    # # print(SERVICE_ACCOUNT_FILE)
    # # import os
    # # print("Current working directory:", os.getcwd())

    # SCOPES = ['https://www.googleapis.com/auth/drive']

    # creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # drive_service = build('drive', 'v3', credentials=creds)

    # folder_metadata = {
    #     'name': 'My OCR Folder',
    #     'mimeType': 'application/vnd.google-apps.folder'
    # }
    # folder = drive_service.files().create(body=folder_metadata, fields='id, name, parents').execute()
    # folder_id = folder.get('id')

    # ocr_output_stream.seek(0)
    # file_metadata = {
    #     'name': pdf_file.filename,
    #     'parents': [folder_id]
    # }
    # media = MediaIoBaseUpload(ocr_output_stream, mimetype='application/pdf')

    # file = drive_service.files().create(body=file_metadata, media_body=media, fields='id, name, parents').execute()
    # file_id = file.get('id')
    
    # return jsonify({'message': 'File uploaded successfully', 'file_id': file_id, 'text_data': text_data}), 200

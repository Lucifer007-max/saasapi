from flask import Blueprint, jsonify, request
from api import db
from .models import Roles  # Make sure to import your Roles model

roleservice = Blueprint('roleservice', __name__)

@roleservice.route('/roles-get', methods=['GET'])
def rolesGet():
    try:
        roles = Roles.query.all()
        return roles, 200
    except Exception as e:
        return _handle_error(e)



def _handle_error(error):
    print(f"Error occurred: {error}")
    return jsonify({'error': str(error)}), 500


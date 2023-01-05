import logging

from flask import Blueprint, request, Response, jsonify

from flaskr.exceptions.apierror import APIError
from flaskr.exceptions.apivalidationerror import APIValidationError
from flaskr.users.models import User

auth_ = Blueprint('auth', __name__)


@auth_.route('sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        user_data = request.get_json()
        if "user_name" not in user_data:
            raise APIValidationError('user name is not given')
        else:
            user_name = user_data['user_name']
            contact_number = user_data['contact_number']
            date_of_birth = user_data['date_of_birth']
            gender = user_data['gender']
            password = user_data['password']
            user = User.query.filter_by(username=user_name).first()
            if user:
                response = Response("User already present", 409, mimetype='application/json')
                return response
            else:
                User.add_user(user_name, contact_number, date_of_birth, gender, password)
                response = Response("User added successfully", 201, mimetype='application/json')
                return response


# @auth_.errorhandler(APIError)
# def handle_exception(err):
#     """Return custom JSON when APIError or its children are raised"""
#     response = {"error": err.description, "status code": err.code, "message": ""}
#     if len(err.args) > 0:
#         response["message"] = err.args[0]
#     # Add some logging so that we can monitor different types of errors
#     logging.error(f'{err.description}: {response["message"]}')
#     return jsonify(response),err.code


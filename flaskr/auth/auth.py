import logging

from flask import Blueprint, request, Response
from flaskr.enums.enum_class import Gender
from flaskr.exceptions.apivalidationerror import ErrorResponse
from flaskr.users.models import User
from flaskr.users.service import add_user
from flaskr.utilfile.utilclass import validate_number, validate_date, validate_name, validate_password

auth_ = Blueprint('auth', __name__)

"""
This method is to create user with given request data

:raise: ErrorResponse if the given data doesn't follow validation conditions.
"""


@auth_.route('sign-up', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        user_data = request.get_json()

        # validation for username

        if "user_name" not in user_data:
            raise ErrorResponse('user name is not given')
        elif user_data['user_name'] is None and not validate_name(user_data['user_name']):
            raise ErrorResponse('enter username with only number and alphabets')
        elif User.query.filter_by(username=user_data['user_name']).first() is not None:
            raise ErrorResponse("User already exist!", 'Already Exist Error')
        else:
            username = user_data['user_name']

        # validation for contact number

        if "contact_number" not in user_data:
            raise ErrorResponse('contact number is not given', 'Validation Error')
        elif user_data['contact_number'] is None and not validate_number(user_data['contact_number']):
            raise ErrorResponse('enter valid contact number', 'Validation Error')
        elif User.query.filter_by(contact_number=user_data['contact_number']).first() is not None:
            raise ErrorResponse('contact number already exist', 'Already Exist Error')
        else:
            contact_number = user_data['contact_number']

        # validation for date of birth

        if "date_of_birth" not in user_data:
            raise ErrorResponse('date of birth is not given', 'Validation Error')
        elif not validate_date(user_data['date_of_birth']):
            raise ErrorResponse('enter valid date of birth', 'Validation Error')
        else:
            date_of_birth = user_data['date_of_birth']

        # validation for gender

        if "gender" not in user_data:
            raise ErrorResponse('gender is not given', 'Validation Error')
        elif not user_data['gender'].lower() in [item.value for item in Gender]:
            logging.error("exception is raised for wrong input!")
            raise ErrorResponse('enter valid gender', 'Validation Error')
        else:
            gender = user_data['gender']

        # validation for password

        if 'password' not in user_data:
            raise ErrorResponse('password is not given', 'Validation Error')
        elif user_data['password'] is not None and not validate_password(user_data['password']):
            raise ErrorResponse("password is invalid!", 'Validation Error')
        else:
            password = user_data['password']
            add_user(username, contact_number, date_of_birth, gender, password)
            response = Response("User added successfully", 201, mimetype='application/json')
            return response

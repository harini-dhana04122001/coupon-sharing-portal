import datetime
import logging

from flask import Blueprint, Response, jsonify, request
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.users.service import get_user_by_contact, get_all_user, delete_user_by_contact, update_user

display = Blueprint('display', __name__)

""" 
this method to get all users 

:return return of user details if user details is not empty else return error response
"""


@display.route('/', methods=['GET'])
def get_users():
    logging.info('ENTERING get_user METHOD')
    user_details = get_all_user()
    if user_details is not None:
        logging.info('EXITING get_users METHOD')
        return jsonify({'User_Details': user_details})
    else:
        logging.error(f'error occurred in get_user method', {request.url_root}, request.get_json())
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


""" 
method to get user by contact number

:return: return of user details if user details is not empty else return error response.
"""


@display.route('/filter-by-contact', methods=['GET'])
def get_by_contact():
    logging.info('ENTERING get_by_contact METHOD')
    contact = request.args.get('contact')
    user_detail_by_contact = get_user_by_contact(contact)
    if user_detail_by_contact is not None:
        logging.info('EXITING get_by_contact METHOD')
        return jsonify({'User_Details': user_detail_by_contact})
    else:
        logging.error(f'error occurred in get_by_contact method : {request.url_root} - {request.get_json()}')
        response = Response("There is no details with this contact number", 404, mimetype='application/json')
        return response


""" 
Delete user by given id  

:arg contact: the argument have contact number of user
:return: response in from of json
"""


@display.route('/<contact>', methods=['DELETE'])
def delete_user_by_contacts(contact):
    logging.info('ENTERING delete_user_by_id METHOD')
    brand = get_user_by_contact(contact)
    delete_user_by_contact(contact)
    if brand:
        response = Response("Deleted Successfully", 200, mimetype='application/json')
        logging.info('EXITING delete_user_by_contact METHOD')
        return response
    else:
        logging.error(f'error occurred in delete_user_by_id method : {request.url_root} - {request.get_json()}')
        response = Response("There is no details with this contact", 404, mimetype='application/json')
        return response


"""
This method is to create user with given request data

:raise: ErrorResponse if the given data doesn't follow validation conditions.
"""


@display.route('/update/<user_id>', methods=['PUT'])
def update_users(user_id):
    if request.method == 'PUT':
        user_data = request.get_json()
        username = user_data['user_name']
        contact_number = user_data['contact_number']
        date_of_birth = user_data['date_of_birth']
        gender = user_data['gender']
        password = user_data['password']
        update_user(user_id, username, contact_number, date_of_birth, gender, password)
        response = Response("User update successfully", 201, mimetype='application/json')
        return response


"""
This method handle exception that are raised for NotFoundException.

:return: response with error description, code, and timestamp in form of json
"""


@display.errorhandler(NotFoundException)
def handle_exception(err):
    """Return custom JSON when APIError are raised"""
    response = {"error": err.description, "status code": 404, "message": "",
                "timestamp": datetime.datetime.now()}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        # Add some logging so that we can monitor different types of errors
        logging.error(f'{err.description} - {request.url_root} - {request.get_data()}: {response["message"]}')
        return jsonify(response), 404

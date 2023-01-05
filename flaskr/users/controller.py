import logging

from flask import Blueprint, Response, jsonify, request
from flaskr.users.models import User

display = Blueprint('display', __name__)


""" method to get all users """


@display.route('/add', methods=['GET'])
def get_users():
    user_details = User.get_all_user()
    if user_details is not None:
        logging.info('RETURNING USER DETAILS')
        return jsonify({'User_Details': user_details})
    else:
        logging.info('RETURNING ERROR MESSAGE')
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


""" method to get user by contact number """


@display.route('/filter-by-contact', methods=['GET'])
def get_by_contact():
    contact = request.args.get('contact')
    user_detail_by_contact = User.get_user_by_contact(contact)
    if user_detail_by_contact is not None:
        logging.info('RETURNING USER DETAILS BY CONTACT')
        return jsonify({'User_Details': user_detail_by_contact})
    else:
        response = Response("There is no details with this contact number", 404, mimetype='application/json')
        return response


""" Delete user by given id  """


@display.route('/<contact>', methods=['DELETE'])
def delete_user_by_id(contact):
    User.delete_user_by_contact(contact)
    brand_deleted = User.get_user_by_contact(contact)
    if brand_deleted :
        response = Response("Deleted Successfully", 200, mimetype='application/json')
        return response
    else:
        response = Response("There is no details with this contact", 404, mimetype='application/json')
        return response

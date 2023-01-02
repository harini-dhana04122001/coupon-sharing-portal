import uuid

from flask import Blueprint, render_template, request, Response, jsonify
from flaskr.user import User
from flaskr.coupon import Coupon

display = Blueprint('display', __name__)


@display.route('user', methods=['POST'])
def create_users():
    user_data = request.get_json()
    user_id = str(uuid.uuid4())
    user_name = user_data['user_name']
    contact_number = user_data['contact_number']
    date_of_birth = user_data['date_of_birth']
    gender = user_data['gender']
    password = user_data['password']
    User.add_user(user_id,user_name,contact_number,date_of_birth,gender, password)
    response = Response("User added successfully", 201, mimetype='application/json')
    return response


@display.route('user', methods=['GET'])
def get_movies():
    user_details = User.get_all_user()
    if user_details is not None:
        return jsonify({'User_Details': user_details})
    else:
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


@display.route('user/<contact>', methods=['GET'])
def get_by_contact(contact):
    user_detail_by_contact = User.get_user_by_contact(contact)
    if user_detail_by_contact is not None:
        return jsonify({'User_Details': user_detail_by_contact})
    else:
        response = Response("There is no details with this contact number", 404, mimetype='application/json')
        return response


@display.route('coupon', methods=['POST'])
def create_coupons():
    user_data = request.get_json()
    coupon_id = str(uuid.uuid4())
    name = user_data['name']
    description = user_data['description']
    offer = user_data['offer']
    coupon_code = user_data['coupon_code']
    price = user_data['price']
    brand_id = user_data['brand_id']
    unique_number = user_data['unique_number']
    expiry_date = user_data['expiry_date']
    image_url = user_data['image_url']
    Coupon.add_user(coupon_id, name, description, offer, coupon_code, price, brand_id, unique_number, expiry_date,
                    image_url)
    response = Response("Coupons added successfully", 201, mimetype='application/json')
    return response


@display.route('coupon', methods=['GET'])
def get_coupons():
    coupon_details = Coupon.get_all_coupons()
    if coupon_details is not None:
        return jsonify({'Coupon_Details': coupon_details})
    else:
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


@display.route('coupon/<brand_id>', methods=['GET'])
def get_by_brand(brand_id):
    coupon_by_brand = Coupon.get_coupon_by_brand(brand_id)
    if coupon_by_brand is not None:
        return jsonify({'Coupon_Details': coupon_by_brand})
    else:
        response = Response("There is no details with this brand", 404, mimetype='application/json')
        return response



import logging
from datetime import datetime

from flask import Blueprint, request, Response, jsonify
from flaskr.coupons.models import Coupon
from flaskr.exceptions.notfoundexception import NotFoundException

display = Blueprint('display', __name__)


""" method to create coupon details """


@display.route('/', methods=['POST'])
def create_coupons():
    user_data = request.get_json()
    user_id = user_data['user_id']
    name = user_data['name']
    description = user_data['description']
    offer = user_data['offer']
    coupon_code = user_data['coupon_code']
    brand_name = user_data['brand_name']
    unique_number = user_data['unique_number']
    expiry_date = user_data['expiry_date']
    price = user_data['price']
    Coupon.add_coupon(user_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date,
                      price)
    response = Response("Coupons added successfully", 201, mimetype='application/json')
    return response


""" method to get all coupon details """


@display.route('/', methods=['GET'])
def get_coupons():
    coupon_details = Coupon.get_all_coupons()
    if coupon_details is not None:
        return jsonify({'Coupon_Details': coupon_details})
    else:
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


""" method to get coupon with given brand name """


@display.route('filter-coupon-by-brand/<brand_name>', methods=['GET'])
def get_by_coupon_by_brand(brand_name):
    coupon_by_brand = Coupon.get_coupon_by_brand(brand_name)
    if coupon_by_brand is not None:
        return jsonify({'Coupon_Details': coupon_by_brand})
    else:
        response = Response("There is no coupon details with this brand", 404, mimetype='application/json')
        return response


@display.route('filter-coupon-by-type/<brand_type>', methods=['GET'])
def get_by_coupon_by_type(brand_type):
    coupon_by_type = Coupon.get_coupon_by_brand_type(brand_type)
    if coupon_by_type is not None:
        return jsonify({'Coupon_Details': coupon_by_type})
    else:
        response = Response("There is no coupon details with this brand", 404, mimetype='application/json')
        return response


@display.route('filter-coupon-by-user/<user_name>', methods=['GET'])
def get_by_coupon_by_user(user_name):
    coupon_by_user = Coupon.get_coupon_by_user(user_name)
    if coupon_by_user is not None:
        return jsonify({'Coupon_Details': coupon_by_user})
    else:
        response = Response("There is no coupon details with this user", 404, mimetype='application/json')
        return response


@display.route('buy-coupon/<coupon_id>/<buyer_id>', methods=['PUT'])
def buy_coupon(coupon_id, buyer_id):
    coupon_bought = Coupon.get_coupon_by_id(coupon_id)
    if coupon_bought is not None:
        Coupon.buy_coupon(coupon_id, buyer_id)
        return jsonify({'Coupon_Details': Coupon.get_coupon_by_id(coupon_id)})
    else:
        response = Response("There is no coupon present", 404, mimetype='application/json')
        return response


@display.errorhandler(NotFoundException)
def handle_exception(err):
    """Return custom JSON when APIError are raised"""
    response = {"error": err.description, "status code": 404, "message": "",
                "timestamp": datetime.now()}
    if len(err.args) > 0:
        response["message"] = err.args[0]
        # Add some logging so that we can monitor different types of errors
        logging.error(f'{err.description} - {request.url_root} - {request.get_data()}: {response["message"]}')
        return jsonify(response), 404

import uuid

from flask import Blueprint, request, Response, jsonify
from flaskr.coupons.models import Coupon

display = Blueprint('display', __name__)


""" method to create coupon details """


@display.route('/', methods=['POST'])
def create_coupons():
    user_data = request.get_json()
    user_id = user_data['user_id']
    coupon_id = str(uuid.uuid4())
    name = user_data['name']
    description = user_data['description']
    offer = user_data['offer']
    coupon_code = user_data['coupon_code']
    brand_name = user_data['brand_name']
    unique_number = user_data['unique_number']
    expiry_date = user_data['expiry_date']
    price = user_data['price']
    Coupon.add_coupon(coupon_id, user_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date,
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
        response = Response("There is no details with this brand", 404, mimetype='application/json')
        return response

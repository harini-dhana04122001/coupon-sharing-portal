from flask import Blueprint, request, Response, jsonify
from flaskr.coupons.service import add_coupon, get_coupon_by_id, get_coupon_by_brand, get_coupon_by_brand_type, \
    get_all_coupons, get_coupon_by_user, buy_coupon, update_coupon

display = Blueprint('display', __name__)


""" 
This method to create brand details 

:raise: ErrorResponse if the given data doesn't follow validation conditions.
"""


@display.route('/', methods=['POST'])
def create_coupons():
    coupon_data = request.get_json()
    user_id = coupon_data['user_id']
    current_user_id = user_id
    name = coupon_data['name']
    description = coupon_data['description']
    offer = coupon_data['offer']
    sale_price = coupon_data['price']
    coupon_url = coupon_data['coupon_url']
    qr_url = coupon_data['qr_url']
    add_coupon(user_id, current_user_id, name, description, offer, sale_price, coupon_url, qr_url)
    response = Response("Coupons added successfully", 201, mimetype='application/json')
    return response


""" 
This method to get all coupon 

:return: return of coupon details if coupon details is not empty else return error response 
"""


@display.route('/', methods=['GET'])
def get_coupons():
    coupon_details = get_all_coupons()
    if coupon_details is not None:
        return jsonify({'Coupon_Details': coupon_details})
    else:
        response = Response("There is no coupon details present in database", 500, mimetype='application/json')
        return response


""" 
method to get all coupon with given brand name 

:return: return of coupon details if coupon with that brand name is found else return error response.
"""


@display.route('filter-coupon-by-brand/<brand_name>', methods=['GET'])
def get_by_coupon_by_brand(brand_name):
    coupon_by_brand = get_coupon_by_brand(brand_name)
    if coupon_by_brand is not None:
        return jsonify({'Coupon_Details': coupon_by_brand})
    else:
        response = Response("There is no coupon details with this brand", 404, mimetype='application/json')
        return response


""" 
method to get all coupon with given brand type 

:return: return of coupon details if coupon with that brand type is found else return error response.
"""


@display.route('filter-coupon-by-type/<brand_type>', methods=['GET'])
def get_by_coupon_by_type(brand_type):
    coupon_by_type = get_coupon_by_brand_type(brand_type)
    if coupon_by_type is not None:
        return jsonify({'Coupon_Details': coupon_by_type})
    else:
        response = Response("There is no coupon details with this brand", 404, mimetype='application/json')
        return response


""" 
method to get all coupon with given username 

:return: return of coupon details if coupon with that username is found else return error response.
"""


@display.route('filter-coupon-by-user/<user_name>', methods=['GET'])
def get_by_coupon_by_user(user_name):
    coupon_by_user = get_coupon_by_user(user_name)
    if coupon_by_user is not None:
        return jsonify({'Coupon_Details': coupon_by_user})
    else:
        response = Response("There is no coupon details with this user id", 404, mimetype='application/json')
        return response


""" 
This method to buy coupon with given coupon id and buyer id.

:return: return of coupon details after the coupon is successfully bought else return error response.
"""


@display.route('buy-coupon/<coupon_id>/<buyer_id>', methods=['PUT'])
def buy_coupons(coupon_id, buyer_id):
    coupon_bought = get_coupon_by_id(coupon_id)
    if coupon_bought is not None:
        buy_coupon(coupon_id, buyer_id)
        return jsonify({'Coupon_Details': get_coupon_by_id(coupon_id)})
    else:
        response = Response("There is no coupon present", 404, mimetype='application/json')
        return response


"""
This method is to update user with given request data

:arg coupon_id: this argument contain id of coupon.
"""


@display.route('/update/<coupon_id>', methods=['PUT'])
def update_users(coupon_id):
    coupon_data = request.get_json()
    if request.method == 'PUT':
        name = coupon_data['name']
        description = coupon_data['description']
        offer = coupon_data['offer']
        coupon_code = coupon_data['coupon_code']
        brand_name = coupon_data['brand_name']
        unique_number = coupon_data['unique_number']
        expiry_date = coupon_data['expiry_date']
        price = coupon_data['price']
        update_coupon(coupon_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date, price)
        response = Response("Coupon update successfully", 201, mimetype='application/json')
        return response


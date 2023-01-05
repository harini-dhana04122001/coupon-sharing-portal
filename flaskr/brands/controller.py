import uuid

from flask import Blueprint, request, Response, jsonify

from flaskr.transactions.models import Transaction
from flaskr.brands.models import Brand


display = Blueprint('display', __name__)

""" method to create brand details """


@display.route('/', methods=['POST'])
def create_brands():
    brand_data = request.get_json()
    brand_name = brand_data['name']
    brand_type = brand_data['type']
    Brand.add_brand(brand_name, brand_type)
    response = Response("Brand added successfully", 201, mimetype='application/json')
    return response


""" method to get all brand """


@display.route('/', methods=['GET'])
def get_brands():
    brand_details = Brand.get_all_brands()
    if brand_details is not None:
        return jsonify({'Brand_Details': brand_details})
    else:
        response = Response("There is no brand details present in database", 500, mimetype='application/json')
        return response


""" method to get all brand with given brand name """


@display.route('/filter-by-name', methods=['GET'])
def get_by_brand():
    brand_name = request.args.get('brand_name')
    brand_by_name = Brand.get_by_brand(brand_name)
    if brand_by_name is not None:
        return jsonify({'User_Details': brand_by_name})
    else:
        response = Response("There is no details with this brand", 404, mimetype='application/json')
        return response


""" method to get all brand with given brand type """


@display.route('/filter-by-type', methods=['GET'])
def get_by_type():
    brand_type = request.args.get('brand_type')
    brand_by_type = Brand.get_by_type(brand_type)
    if brand_by_type is not None:
        return jsonify({'User_Details': brand_by_type})
    else:
        response = Response("There is no details with this type", 404, mimetype='application/json')
        return response


""" method to update brand with given brand id """


@display.route('/<brand_id>', methods=['PUT'])
def update_by_value(brand_id):
    brand_data = request.get_json()
    print(brand_data)
    if 'name' and 'type' in brand_data.keys():
        brand_name = brand_data['name']
        brand_type = brand_data['type']
        key = "both"
        Brand.update_brand(brand_id, key, brand_name, brand_type)
        response = Response("Brand updated successfully", 200, mimetype='application/json')
        return response
    elif 'name' in brand_data.keys():
        brand_name = brand_data['name']
        key = 'name'
        Brand.update_brand(brand_id, key, brand_name)
        response = Response("Brand name updated successfully", 200, mimetype='application/json')
        return response
    elif 'type' in brand_data:
        brand_type = brand_data['type']
        key = 'type'
        Brand.update_brand(brand_id, key, brand_type)
        response = Response("Brand type updated successfully", 200, mimetype='application/json')
        return response

    else:
        response = Response("Brand not found", 404, mimetype='application/json')
        return response


""" method to soft delete brand with given brand id """


@display.route('/<brand_id>', methods=['DELETE'])
def delete_brand_by_id(brand_id):
    Brand.delete_brand(brand_id)
    brand_deleted = Brand.query.filter_by(id=brand_id, is_active=False).first()
    if brand_deleted is not None:
        response = Response("Deleted Successfully", 200, mimetype='application/json')
        return response
    else:
        response = Response("There is no details with this brand id", 404, mimetype='application/json')
        return response


""" method to buy coupon """


@display.route('/<coupon_id>', methods=['POST'])
def buy_coupon():
    buying_data = request.get_json()
    coupon_id = str(uuid.uuid4())
    buyer_id = buying_data['buyer_id']
    price = buying_data['price']
    Transaction.buy_coupons(coupon_id, buyer_id, price)
    response = Response("Coupons added successfully", 201, mimetype='application/json')
    return response

import datetime
import logging
import uuid

from flask import Blueprint, request, Response, jsonify

from flaskr.brands.models import Brand
from flaskr.brands.service import add_brand, get_all_brands, get_by_brand, get_by_type, update_brand, delete_brand
from flaskr.exceptions.apivalidationerror import ErrorResponse
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.transactions.models import Transaction
from flaskr.utilfile.utilclass import validate_name

display = Blueprint('display', __name__)

""" 
this method to create brand details 

:raise: ErrorResponse if the given data doesn't follow validation conditions.
"""


@display.route('/', methods=['POST'])
def create_brands():
    brand_data = request.get_json()
    if "name" not in brand_data:
        raise ErrorResponse('brand name is not given')
    else:
        if not validate_name(brand_data['name']):
            raise ErrorResponse('enter brand name with only number and alphabets')
        elif brand_data['name'] is None:
            raise ErrorResponse('brand name is empty')
        else:
            brand_name = brand_data['name']

    if "type" not in brand_data:
        raise ErrorResponse('brand type is not given')
    else:
        if not validate_name(brand_data['type']):
            raise ErrorResponse('enter brand type with only alphabets')
        elif brand_data['type'] is None:
            raise ErrorResponse('brand type is empty')
        else:
            brand_type = brand_data['type']
            if Brand.query.filter_by(name=brand_name).first() is not None:
                raise ErrorResponse('brand already present in database')
            add_brand(brand_name, brand_type)
            response = Response("Brand added successfully", 201, mimetype='application/json')
            return response


""" 
this method to get all brand 

:return: return of brand details if brand details is not empty else return error response
"""


@display.route('/', methods=['GET'])
def get_brands():
    brand_details = get_all_brands()
    if brand_details is not None:
        logging.info('Exiting get_brands method')
        return jsonify({'Brand_Details': brand_details})
    else:
        logging.error(f'error occurred in get_user method', {request.url_root}, request.get_json())
        response = Response("There is no brand details present in database", 500, mimetype='application/json')
        return response


""" 
method to get all brand with given brand name 

:return: return of brand details if brand details is not empty else return error response.
"""


@display.route('/filter-by-name', methods=['GET'])
def get_by_brands():
    brand_name = request.args.get('brand_name')
    brand_by_name = get_by_brand(brand_name)
    if brand_by_name is not None:
        return jsonify({'User_Details': brand_by_name})
    else:
        response = Response("There is no details with this brand", 404, mimetype='application/json')
        return response


""" 
method to get all brand with given brand type 

:return: response in json form with the given brand type
"""


@display.route('/filter-by-type', methods=['GET'])
def get_by_types():
    brand_type = request.args.get('brand_type')
    brand_by_type = get_by_type(brand_type)
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
        update_brand(brand_id, key, brand_name, brand_type)
        response = Response("Brand updated successfully", 200, mimetype='application/json')
        return response
    elif 'name' in brand_data.keys():
        brand_name = brand_data['name']
        key = 'name'
        update_brand(brand_id, key, brand_name)
        response = Response("Brand name updated successfully", 200, mimetype='application/json')
        return response
    elif 'type' in brand_data:
        brand_type = brand_data['type']
        key = 'type'
        update_brand(brand_id, key, brand_type)
        response = Response("Brand type updated successfully", 200, mimetype='application/json')
        return response

    else:
        response = Response("Brand not found", 404, mimetype='application/json')
        return response


""" method to soft delete brand with given brand id """


@display.route('/<brand_id>', methods=['DELETE'])
def delete_brand_by_id(brand_id):
    logging.info('ENTERING delete_user_by_id METHOD')
    brand_deleted = delete_brand(brand_id)
    if brand_deleted is not None:
        response = Response("Deleted Successfully", 200, mimetype='application/json')
        logging.info('EXITING delete_user_by_id METHOD')
        return response
    else:
        logging.error(f'error occurred in delete_brand_by_id method : {request.url_root} - {request.get_json()}')
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

import datetime
import logging

from flask import Blueprint, Response, jsonify, request
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.transactions.service import get_all_transactions,get_by_transaction_coupon_id

display = Blueprint('display', __name__)


""" 
this method to get all transaction 

:return: return of transaction details if transaction details is not empty else return error response
"""


@display.route('/', methods=['GET'])
def get_transactions():
    transaction_details = get_all_transactions()
    if transaction_details is not None:
        return jsonify({'Transaction-Details': transaction_details})
    else:
        response = Response("There is no transaction details present in database", 500, mimetype='application/json')
        return response


""" 
method to get all transaction with given coupon id

:return: return of transaction details if transaction details is not empty else return error response.
"""


@display.route('/coupon/<coupon_id>', methods=['GET'])
def get_transaction_by_coupon(coupon_id):
    transaction_details = get_by_transaction_coupon_id(coupon_id)
    if transaction_details is not None:
        return jsonify({'Transaction-Details': transaction_details})
    else:
        response = Response("There is no transaction details present in database", 500, mimetype='application/json')
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
        # Adding some logging so that we can monitor different types of errors
        logging.error(f'{err.description} - {request.url_root} - {request.get_data()}: {response["message"]}')
        return jsonify(response), 404

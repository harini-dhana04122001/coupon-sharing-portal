from flask import Blueprint,Response, jsonify
from flaskr.transactions.models import Transaction

display = Blueprint('display', __name__)


""" method to get all coupon details """


@display.route('/', methods=['GET'])
def get_transactions():
    transaction_details = Transaction.get_all_transactions()
    if transaction_details is not None:
        return jsonify({'Transaction-Details': transaction_details})
    else:
        response = Response("There is no transaction details present in database", 500, mimetype='application/json')
        return response


@display.route('/coupon/<coupon_id>', methods=['GET'])
def get_transaction_by_coupon(coupon_id):
    transaction_details = Transaction.get_by_transaction_coupon_id(coupon_id)
    if transaction_details is not None:
        return jsonify({'Transaction-Details': transaction_details})
    else:
        response = Response("There is no transaction details present in database", 500, mimetype='application/json')
        return response

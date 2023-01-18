import pickle

from flaskr.app import db
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.enums.enum_class import TransactionStatus
from flaskr.transactions.models import Transaction
from flaskr.users.service import get_user_by_id

"""
This method takes in data and display it in form of dictionary

:return: The result after inserting the data in the dictionary
:rtype: dict
"""


def json(data):
    from flaskr.coupons.service import get_coupon_by_id
    if data is not None:
        return {'transaction_id': data.id, 'coupon_id': get_coupon_by_id(data.coupon_id),
                'buyer': get_user_by_id(data.buyer_id), 'seller': get_user_by_id(data.seller_id),
                'status': data.status, 'coupon_price': data.coupon_price}
    else:
        raise NotFoundException('the transaction details are not present in the database')


"""
This method takes in transaction details and store them in database.

:param status: this argument takes status of transaction
:param coupon_id: this arguments takes coupon id of the transaction
:param buyer_id: this arguments takes buyer id for the transaction
:param seller_id: this arguments takes seller id for the transaction
:param coupon_price: this arguments takes in coupon price of the transaction
"""


def create_transaction(status, coupon_id, buyer_id, seller_id, coupon_price):
    if status in [item.value for item in TransactionStatus]:
        created_by = pickle.dumps(get_user_by_id(buyer_id))
        db.session.add(Transaction(TransactionStatus(status).name, coupon_id, buyer_id, seller_id,
                                   coupon_price, created_by))
        db.session.commit()


"""
This method displays all the transaction which is present in database

:return: The result after getting the data from the database and adding it to list
:rtype: list(dict)
"""


def get_all_transactions():
    return [json(transaction) for transaction in Transaction.query.all()]


"""
This method displays user with the given coupon id

:return: The result after getting the data from the database with the given coupon id
:rtype: dict
"""


def get_by_transaction_coupon_id(coupon_id):
    return [json(transaction) for transaction in Transaction.query.filter_by(coupon_id=coupon_id).all()]

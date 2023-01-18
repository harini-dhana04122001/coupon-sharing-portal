from datetime import datetime
import pickle

from flaskr.app import db
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.coupons.models import Coupon
from flaskr.payments.models import Payment
from flaskr.transactions.service import create_transaction
from flaskr.users.service import get_user_by_id, get_user_by_username
from flaskr.brands.service import get_by_brand, get_by_id, get_by_type

"""
This method takes in data and display it in form of dictionary

:return: The result after inserting the data in the dictionary
:rtype: dict
"""


def coupon_json(data):
    if data is not None:
        return {'id': data.id, 'coupon_name': data.name,
                'description': data.description, 'offer': data.offer,
                'coupon_code': data.coupon_code, 'brand': get_by_id(data.brand_id),
                'qr/bar code': data.coupon_key, 'user': get_user_by_id(data.user_id),
                'expiry_date': data.expiry_date, 'price': data.sale_price}
    else:
        raise NotFoundException('the given coupon data is not present in database')


"""
    This method takes in coupon details and store them in database.

    :param user_id: contains id of user
    :param current_user_id: contain id of current coupon owner
    :param name: contains coupon name
    :param description: contains coupon description
    :param offer: contains coupon offer
    :param coupon_code: contains coupon code
    :param brand_name: contains name of the brand of the coupon
    :param unique_number: contain converted unique_number
    :param expiry_date: contain expiry date of the coupon
    :param sale_price: contains price of coupon
"""


def add_coupon(user_id, current_user_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date,
               sale_price):
    brand_by_name = get_by_brand(brand_name)
    coupon = Coupon(user_id, current_user_id, name, description, offer, coupon_code, sale_price, brand_by_name['id'],
                    unique_number, expiry_date)

    coupon.created_by = pickle.dumps(get_user_by_id(user_id))
    coupon.updated_by = coupon.created_by
    if brand_by_name is not None:
        db.session.add(coupon)
        db.session.commit()


"""
This method displays all the coupons which is present in database

:return: The result after getting the data from the database and adding it to list
:rtype: list(dict)
"""


def get_all_coupons():
    return [coupon_json(coupon) for coupon in Coupon.query.all()]


"""
This method displays coupon with the given brand name

:return: The result after getting the data from the database with the given brand name
:rtype: dict
"""


def get_coupon_by_brand(brand_name):
    brand_by_name = get_by_brand(brand_name)
    return [coupon_json(coupon) for coupon in Coupon.query.filter_by(brand_id=brand_by_name['id']).all()]


"""
This method displays coupon with the given brand type

:return: The result after getting the data from the database with the given brand type
:rtype: list(dict)
"""


def get_coupon_by_brand_type(brand_type):
    brand_by_type = get_by_type(brand_type)
    # store the id of every brand that matches the given type
    ids = [brand['id'] for brand in brand_by_type]
    return [coupon_json(coupon) for coupon in Coupon.query.filter(Coupon.id.in_(ids)).all()]


"""
This method displays coupon with the given coupon id

:return: The result after getting the data from the database with the given coupon id
:rtype: dict
"""


def get_coupon_by_id(coupon_id):
    coupon_by_id = coupon_json(Coupon.query.filter_by(id=coupon_id).first())
    return coupon_by_id


"""
This method displays coupon with the given user name

:return: The result after getting the data from the database with the given user name
:rtype: dict
"""


def get_coupon_by_user(user_name):
    brand_by_user = get_user_by_username(user_name)

    coupon_by_user_id = coupon_json(Coupon.query.filter_by(user_id=brand_by_user['id']).first())
    if coupon_by_user_id is not None:
        return coupon_by_user_id


"""
This method is to update user details.

:param user_id: this contains the id of user
:param username: this contains the name of user
:param contact_number: this contains the contact number of user
:param date_of_birth: this contains the date of birth of user
:param gender: this contains the gender of user
:param password: this contains the password of user
"""


def update_coupon(coupon_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date, price):
    coupon = Coupon.query.filter_by(id=coupon_id).first()
    if name is not None:
        coupon.name = name

    if description is not None:
        coupon.description = description

    if offer is not None:
        coupon.offer = offer

    if coupon_code is not None:
        coupon.coupon_code = coupon_code

    if brand_name is not None:
        brand_by_name = get_by_brand(brand_name)
        coupon.brand_id = brand_by_name['id']

    if unique_number is not None:
        coupon.coupon_key = unique_number

    if expiry_date is not None:
        coupon.expiry_date = expiry_date

    if price is not None:
        coupon.sale_price = price

    coupon.updated_on = datetime.now()
    coupon.updated_by = pickle.dumps(coupon.user_id)
    db.session.commit()


"""
This method is to purchase coupon by giving coupon and buyer id. 
This method after successful purchase generate transaction details for the purchase.

:return: The result after getting the data from the database with the given brand name
:rtype: dict
"""


def buy_coupon(coupon_id, buyer_id):
    payment_status = Payment.pay().lower()
    if payment_status == 'successful':
        coupon_by_id = Coupon.query.filter_by(id=coupon_id).first()
        seller_id = coupon_by_id.current_user_id
        coupon_price = coupon_by_id.sale_price
        coupon_by_id.current_user_id = buyer_id
        coupon_by_id.updated_on = datetime.now()
        db.session.commit()
        status = 1
        create_transaction(status, coupon_id, buyer_id, seller_id, coupon_price)


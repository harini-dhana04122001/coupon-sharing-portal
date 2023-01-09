import logging
import pickle
from datetime import datetime
from flaskr import db
from passlib.apps import custom_app_context as pwd_context

from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.utilfile.utilclass import calculate_age


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    contact_number = db.Column(db.String(), unique=True)
    date_of_birth = db.Column(db.DateTime)
    gender = db.Column(db.String())
    password_hash = db.Column(db.String())
    coupons = db.relationship('Coupon', backref='user', lazy=True)
    buyer_transaction = db.relationship('Transaction', foreign_keys="Transaction.buyer_id", lazy=True)
    seller_transaction = db.relationship('Transaction', foreign_keys="Transaction.seller_id", lazy=True)
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    created_by = db.Column(db.PickleType())
    updated_by = db.Column(db.PickleType())
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, contact_number, date_of_birth, gender, created_on=datetime.now(),
                 updated_on=datetime.now()):
        self.username = name
        self.contact_number = contact_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.created_on = created_on
        self.updated_on = updated_on
        self.created_by = pickle.dumps(self)
        self.updated_by = pickle.dumps(self)

    """
    This method takes in password and sets encrypted password
    
    :arg password: the argument have password of user
    """

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    """
    This method takes in password and check if the password is right

    :arg password: the argument have password of user
    :return: The true if the password is correct and false if its not correct.
    """

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)



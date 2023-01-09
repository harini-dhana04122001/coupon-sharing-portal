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

    """
    This method takes in data and display it in form of dictionary
    
    :return: The result after inserting the data in the dictionary
    :rtype: dict
    """

    def display(self):
        logging.info('Entering into add_user method!')
        if self is not None:
            return {'id': self.id, 'username': self.username,
                    'contact_number': self.contact_number, 'age': calculate_age(self.date_of_birth),
                    'gender': self.gender, 'created_by': pickle.loads(self.created_by).username}
        else:
            raise NotFoundException('the given data is not present in database')

    """
    This method takes in user details and store them in database.

    :arg username: the argument have name of user.
    :arg contact_number: the argument have contact of user.
    :arg date_of_birth: the argument have date of birth of user.
    :arg gender: the argument have gender of user.
    :arg password: the argument have password of user.
    """

    @staticmethod
    def add_user(username, contact_number, date_of_birth, gender, password):
        logging.info('ENTERING INTO add_user METHOD!')
        date_of_birth_ = datetime.strptime(date_of_birth, '%d/%m/%Y').date()
        user = User(username, contact_number, date_of_birth_, gender,
                    created_on=datetime.now(), updated_on=datetime.now())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        logging.info('SAVED USER DETAILS TO DATABASE')

    """
    This method displays all the user which is present in database

    :return: The result after getting the data from the database and adding it to list
    :rtype: list(dict)
    """

    @staticmethod
    def get_all_user():
        logging.info("ENTERING INTO get_all_user METHOD")
        users = User.query.filter_by(is_active=True)
        return [User.display(user) for user in users.all()]

    """
    This method displays user with the given contact number

    :return: The result after getting the data from the database with the given contact number
    :rtype: dict
    """

    @staticmethod
    def get_user_by_contact(phone):
        logging.info("ENTERING INTO get_user_by_contact METHOD")
        return User.display(User.query.filter_by(contact_number=phone, is_active=True).first())

    """
    This method displays user with the given contact number

    :return: The result after getting the data from the database with the given contact number
    :rtype: dict
    """

    @staticmethod
    def get_user_by_username(username):
        logging.info("ENTERING INTO get_user_by_contact METHOD")
        return User.display(User.query.filter_by(username=username, is_active=True).first())

    """
    This method displays user with the given id

    :return: The result after getting the data from the database with the given id
    :rtype: dict
    """

    @staticmethod
    def get_user_by_id(user_id):
        logging.info("ENTERING INTO get_user_by_id METHOD")
        return User.display(User.query.filter_by(id=user_id, is_active=True).first())

    """
    This method delete user with the given contact

    :arg contact: the argument have phone number of user.
    """

    @staticmethod
    def delete_user_by_contact(contact):
        logging.info("ENTERING INTO delete_user_by_contact METHOD")
        user_by_contact = User.query.filter_by(contact_number=contact, is_active=True).first()
        user_by_contact.is_active = False
        user_by_contact.updated_on = datetime.now()
        db.session.commit()

    """
    This method update brand with given brand id

    :arg brand_id: the argument have brand id
    :arg key: it have the key with which we can update the brand
    :arg *args: it can have multiple argument.
    """

    @staticmethod
    def update_user(user_id, username, contact_number, date_of_birth, gender, password):
        user = User.query.filter_by(id=user_id, is_active=True).first()
        a = User(username, contact_number, date_of_birth, gender)
        if username is not None:
            user.username = username
            user.updated_on = datetime.now()
            user.updated_by = User

        if contact_number is not None:
            user.contact_number = contact_number
            user.updated_on = datetime.now()
            user.updated_by = User

        if date_of_birth is not None:
            user.date_of_birth = date_of_birth
            user.updated_on = datetime.now()
            user.updated_by = User

        if gender is not None:
            user.gender = gender
            user.updated_on = datetime.now()
            user.updated_by = User

        if password is not None:
            a.hash_password(password)
            user.updated_on = datetime.now()
            user.updated_by = User
        db.session.commit()

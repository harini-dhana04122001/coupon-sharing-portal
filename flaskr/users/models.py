import logging
from datetime import datetime
from flaskr import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    contact_number = db.Column(db.String(), unique=True)
    emailid = db.Column(db.String())
    date_of_birth = db.Column(db.String())
    gender = db.Column(db.String())
    password = db.Column(db.String())
    created_on = db.Column(db.DateTime)
    updated_on = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, contact_number, date_of_birth, gender, password, created_on, updated_on):
        self.username = name
        self.contact_number = contact_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.password = password
        self.created_on = created_on
        self.updated_on = updated_on

    """
    This method takes in data and display it in form of dictionary
    
    :return: The result after inserting the data in the dictionary
    :rtype: dict
    """

    def display(self):
        logging.info('Entering into add_user method!')
        return {'id': self.id, 'username': self.username,
                'contact_number': self.contact_number, 'date_of_birth': self.date_of_birth,
                'gender': self.gender}

    """
    This method takes in data and display it in form of dictionary

    :return: The result after inserting the data in the dictionary
    :rtype: dict
    """

    @staticmethod
    def add_user(username, contact_number, date_of_birth, gender, password):
        logging.info('ENTERING INTO add_user METHOD!')
        db.session.add(User(username, contact_number, date_of_birth, gender, password,
                            created_on=datetime.now(), updated_on=datetime.now()))
        db.session.commit()
        logging.info('SAVED USER DETAILS TO DATABASE')

    @staticmethod
    def get_all_user():
        logging.info("ENTERING INTO get_all_user METHOD")
        return [User.display(user) for user in User.query.filter_by(is_active=True).all()]

    @staticmethod
    def get_user_by_contact(contact):
        logging.info("ENTERING INTO get_user_by_contact METHOD")
        return User.display(User.query.filter_by(contact_number=contact, is_active=True).first())

    @staticmethod
    def get_user_by_id(user_id):
        logging.info("ENTERING INTO get_user_by_id METHOD")
        return User.display(User.query.filter_by(id=user_id, is_active=True).first())

    @staticmethod
    def delete_user_by_contact(contact):
        logging.info("ENTERING INTO delete_user_by_contact METHOD")
        # User.json(User.query.filter_by(contact_number=contact, is_active=True).first())
        user_by_contact = User.query.filter_by(contact_number=contact, is_active=True).first()
        user_by_contact.is_active = False
        db.session.commit()

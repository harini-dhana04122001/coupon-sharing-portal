from datetime import datetime
import logging
import pickle

from flaskr import NotFoundException, db
from flaskr.users.models import User
from flaskr.utilfile.utilclass import calculate_age

"""
This method takes in data and display it in form of dictionary

:return: The result after inserting the data in the dictionary
:rtype: dict
"""


def display(data):
    logging.info('Entering into add_user method!')
    if data is not None:
        return {'id': data.id, 'username': data.username,
                'contact_number': data.contact_number, 'age': calculate_age(data.date_of_birth),
                'gender': data.gender, 'created_by': pickle.loads(data.created_by).username}
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


def get_all_user():
    logging.info("ENTERING INTO get_all_user METHOD")
    users = User.query.filter_by(is_active=True)
    return [display(user) for user in users.all()]


"""
This method displays user with the given contact number

:return: The result after getting the data from the database with the given contact number
:rtype: dict
"""


def get_user_by_contact(phone):
    logging.info("ENTERING INTO get_user_by_contact METHOD")
    return display(User.query.filter_by(contact_number=phone, is_active=True).first())


"""
This method displays user with the given contact number

:return: The result after getting the data from the database with the given contact number
:rtype: dict
"""


def get_user_by_username(username):
    logging.info("ENTERING INTO get_user_by_contact METHOD")
    return display(User.query.filter_by(username=username, is_active=True).first())


"""
This method displays user with the given id

:return: The result after getting the data from the database with the given id
:rtype: dict
"""


def get_user_by_id(user_id):
    logging.info("ENTERING INTO get_user_by_id METHOD")
    return display(User.query.filter_by(id=user_id, is_active=True).first())


"""
This method delete user with the given contact

:arg contact: the argument have phone number of user.
"""


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

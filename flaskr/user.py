import uuid
from datetime import datetime
from flaskr import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.String(), unique=True)
    user_name = db.Column(db.String())
    contact_number = db.Column(db.String(),unique=True)
    date_of_birth = db.Column(db.String())
    gender = db.Column(db.String())
    password = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, user_id, name, contact_number, date_of_birth, gender, password):
        self.user_id = user_id
        self.user_name = name
        self.contact_number = contact_number
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.password = password

    def json(self):
        return {'id': self.user_id, 'user_name': self.user_name,
                'contact_number': self.contact_number, 'age': self.date_of_birth,
                'gender': self.gender}

    @staticmethod
    def add_user(user_id, user_name, contact_number, date_of_birth, gender, password):
        db.session.add(User(user_id, user_name, contact_number, date_of_birth, gender, password))
        db.session.commit()

    @staticmethod
    def get_all_user():
        return [User.json(user) for user in User.query.all()]

    @staticmethod
    def get_user_by_contact(contact):
        return [User.json(User.query.filter_by(contact_number=contact).first())]

from datetime import datetime

from sqlalchemy import ForeignKey

from flaskr import db
from flaskr.brands.models import Brand
from datetime import datetime
from flaskr import db


class Coupon(db.Model):
    __tablename__ = "coupon"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id'))
    name = db.Column(db.String())
    description = db.Column(db.String())
    offer = db.Column(db.String())
    coupon_code = db.Column(db.String())
    price = db.Column(db.Float())
    brand_id = db.Column(db.Integer(), ForeignKey("brand.id"), nullable=False)
    coupon_key = db.Column(db.String())
    expiry_date = db.Column(db.String())
    image_url = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())
    transactions = db.relationship('Transaction', backref='coupon')


    def __init__(self, user_id, name, description, offer, coupon_code, price, brand_id, unique_number,
                 expiry_date):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.offer = offer
        self.coupon_code = coupon_code
        self.price = price
        self.brand_id = brand_id
        self.unique_number = unique_number
        self.expiry_date = expiry_date

    def json(self):
        return {'id': self.id, 'coupon_name': self.name, 'coupon_holder': self.user_id,
                'description': self.description, 'offer': self.offer,
                'coupon_code': self.coupon_code, 'brand': self.brand_id,
                'qr/bar code': self.unique_number,
                'expiry_date': self.expiry_date, 'price': self.price}

    @staticmethod
    def add_coupon(user_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date,
                   price):
        brand_by_name = Brand.json(Brand.query.filter_by(name=brand_name, is_active=True).first())
        print(brand_by_name)
        if brand_by_name is not None:
            db.session.add(Coupon(user_id, name, description, offer, coupon_code, brand_by_name['id'],
                                  unique_number, expiry_date, price))
            db.session.commit()

    @staticmethod
    def get_all_coupons():
        return [Coupon.json(coupon) for coupon in Coupon.query.all()]

    @staticmethod
    def get_coupon_by_brand(brand_name):
        brand_by_name = Brand.get_by_brand(brand_name)
        if brand_by_name is not None:
            return [Coupon.json(Coupon.query.get(brand_by_name['id']))]

    @staticmethod
    def get_coupon_by_id(coupon_id):
        coupon_by_id = Coupon.json(Coupon.query.filter_by(coupon_id=coupon_id).first())
        if coupon_by_id is not None:
            return coupon_by_id

    @staticmethod
    def get_coupon_by_user_id(user_id):
        coupon_by_user_id = Coupon.json(Coupon.query.filter_by(user_id=user_id).all())
        if coupon_by_user_id is not None:
            return coupon_by_user_id

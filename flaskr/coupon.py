import uuid
from datetime import datetime
from flaskr import db


class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer(), primary_key=True)
    coupon_id = db.Column(db.String(), unique=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    offer = db.Column(db.String())
    coupon_code = db.Column(db.String())
    price = db.Column(db.Float())
    brand_id = db.Column(db.Integer())
    unique_number = db.Column(db.String())
    expiry_date = db.Column(db.String())
    image_url = db.Column(db.String())
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, coupon_id, name, description, offer, coupon_code, price, brand_id, unique_number, expiry_date,
                 image_url):
        self.coupon_id = coupon_id
        self.name = name
        self.description = description
        self.offer = offer
        self.coupon_code = coupon_code
        self.price = price
        self.brand_id = brand_id
        self.unique_number = unique_number
        self.expiry_date = expiry_date
        self.image_url = image_url

    def json(self):
        return {'id': self.coupon_id, 'name': self.name,
                'description': self.description, 'offer': self.offer,
                'coupon_code': self.coupon_code, 'brand': self.brand_id,
                'qr/bar code': self.unique_number,
                'expiry_date': self.expiry_date, 'price': self.price}

    @staticmethod
    def add_user(coupon_id, name, description, offer, coupon_code, brand_id, unique_number, expiry_date, price):
        db.session.add(Coupon(coupon_id, name, description, offer, coupon_code, brand_id, unique_number, expiry_date,
                              price))
        db.session.commit()

    @staticmethod
    def get_all_coupons():
        return [Coupon.json(coupon) for coupon in Coupon.query.all()]

    @staticmethod
    def get_coupon_by_brand(brand_id):
        return [Coupon.json(Coupon.query.filter_by(brand_id=brand_id).first())]

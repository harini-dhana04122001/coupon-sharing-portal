from sqlalchemy import ForeignKey

from datetime import datetime
from flaskr.app import db


class Coupon(db.Model):
    __tablename__ = "coupon"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id'))
    current_user_id = db.Column(db.Integer(), ForeignKey('user.id'))
    name = db.Column(db.String())
    description = db.Column(db.String())
    offer = db.Column(db.String())
    coupon_code = db.Column(db.String())
    sale_price = db.Column(db.Float())
    brand_id = db.Column(db.Integer(), ForeignKey("brand.id"), nullable=False)
    coupon_key = db.Column(db.String())
    expiry_date = db.Column(db.String())
    image_url = db.Column(db.String())
    is_sellable = db.Column(db.Boolean, default=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.PickleType())
    updated_by = db.Column(db.PickleType())
    transactions = db.relationship('Transaction', backref='coupon')
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, current_user_id, name, description, offer, coupon_code, price, brand_id, unique_number,
                 expiry_date, img_url):
        self.user_id = user_id
        self.current_user_id = current_user_id
        self.name = name
        self.description = description
        self.offer = offer
        self.coupon_code = coupon_code
        self.sale_price = price
        self.brand_id = brand_id
        self.coupon_key = unique_number
        self.expiry_date = expiry_date
        self.image_url = img_url
        self.created_on = datetime.now()
        self.updated_on = datetime.now()


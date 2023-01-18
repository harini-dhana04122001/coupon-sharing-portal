from datetime import datetime
from flaskr.app import db


class Brand(db.Model):
    __tablename__ = "brand"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    types = db.Column(db.String())
    coupons = db.relationship('Coupon', backref='brand', lazy=True)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, name, types):
        self.name = name
        self.types = types

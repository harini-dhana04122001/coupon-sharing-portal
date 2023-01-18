from datetime import datetime

from sqlalchemy import ForeignKey

from flaskr.app import db


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer(), primary_key=True)
    status = db.Column(db.String)
    coupon_id = db.Column(db.Integer(), ForeignKey("coupon.id"))
    buyer_id = db.Column(db.Integer(), ForeignKey("user.id"))
    seller_id = db.Column(db.Integer(), ForeignKey("user.id"))
    coupon_price = db.Column(db.Float())
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())
    created_by = db.Column(db.PickleType())

    def __init__(self, status, coupon_id, buyer_id, seller_id,
                 price, created_by):
        self.status = status
        self.coupon_id = coupon_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.coupon_price = price
        self.created_by = created_by

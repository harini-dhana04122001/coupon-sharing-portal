import pickle
from datetime import datetime

from sqlalchemy import ForeignKey

from flaskr import db
from flaskr.enums.enum_class import TransactionStatus
from flaskr.users.models import User


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

    def json(self):
        from flaskr.coupons.models import Coupon
        return {'transaction_id': self.id, 'coupon_id': Coupon.get_coupon_by_id(self.coupon_id),
                'buyer': User.get_user_by_id(self.buyer_id), 'seller': User.get_user_by_id(self.seller_id),
                'status': self.status, 'coupon_price': self.coupon_price}

    @staticmethod
    def create_transaction(status, coupon_id, buyer_id, seller_id, coupon_price):
        # coupon_selected = Coupon.get_coupon_by_id(coupon_id)
        if status in [item.value for item in TransactionStatus]:
            created_by = pickle.dumps(User.get_user_by_id(buyer_id))
            db.session.add(Transaction(status, coupon_id, buyer_id, seller_id,
                                       coupon_price, created_by))
            db.session.commit()

    @staticmethod
    def get_all_transactions():
        return [Transaction.json(transaction) for transaction in Transaction.query.all()]

    @staticmethod
    def get_by_transaction_coupon_id(coupon_id):
        return [Transaction.json(transaction) for transaction in Transaction.query.
                filter_by(coupon_id=coupon_id).all()]

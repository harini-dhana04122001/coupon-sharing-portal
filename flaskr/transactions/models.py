import uuid
from datetime import datetime

from sqlalchemy import ForeignKey

from flaskr import db
from flaskr.brands.models import Brand
from flaskr.coupons.models import Coupon
from flaskr.payments.models import Payment


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer(), primary_key=True)
    types = db.Column(db.String())
    coupon_id = db.Column(db.Integer(), ForeignKey("coupon.id"))
    buyer_id = db.Column(db.Integer(), ForeignKey("user.id"))
    seller_id = db.Column(db.Integer(), ForeignKey("user.id"))
    coupon_type = db.Column(db.String())
    price = db.Column(db.Float())
    is_successful = db.Column(db.Boolean)
    is_redeemed = db.Column(db.Boolean, default=False)
    created_on = db.Column(db.DateTime, default=datetime.now())
    updated_on = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, transaction_id, types, coupon_id, buyer_id, seller_id,
                 coupon_type, price, is_successful):
        self.transaction_id = transaction_id
        self.types = types
        self.coupon_id = coupon_id
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.coupon_type = coupon_type
        self.price = price
        self.is_successful = is_successful

    def json(self):
        return {'transaction_id': self.transaction_id, 'coupon_id': self.coupon_id,
                'buyer_id': self.buyer_id, 'seller_id': self.seller_id, 'type': self.coupon_type,
                'price': self.price}

    @staticmethod
    def buy_coupons(coupon_id, buyer_id, price):
        payment_detail = Payment.pay()
        if payment_detail.lower() == 'successful':
            transaction_id = uuid.uuid4()
            coupon_selected = Coupon.get_coupon_by_id(coupon_id)
            types = coupon_selected['brand_type']
            seller_id = coupon_selected['coupon_holder']
            coupon_type = Brand.get_by_id(coupon_selected['brand'])
            is_successful = True
            db.session.add(Transaction(transaction_id, types, coupon_id, buyer_id, seller_id,
                           coupon_type, price, is_successful))
            db.session.commit()

    @staticmethod
    def get_all_coupon_history():
        return [Transaction.json(history) for history in Transaction.query.all()]

    @staticmethod
    def get_by_history_user_id(user_id):
        return Transaction.json(Transaction.query.filter_by(seller_id=user_id).all())

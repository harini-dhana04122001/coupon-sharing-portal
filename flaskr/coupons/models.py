import pickle

from sqlalchemy import ForeignKey

from flaskr.brands.models import Brand
from datetime import datetime
from flaskr import db
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.payments.models import Payment
from flaskr.transactions.models import Transaction
from flaskr.users.models import User


class Coupon(db.Model):
    __tablename__ = "coupon"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), ForeignKey('user.id'))
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

    def __init__(self, user_id, name, description, offer, coupon_code, price, brand_id, unique_number,
                 expiry_date):
        self.user_id = user_id
        self.name = name
        self.description = description
        self.offer = offer
        self.coupon_code = coupon_code
        self.sale_price = price
        self.brand_id = brand_id
        self.coupon_key = unique_number
        self.expiry_date = expiry_date
        self.created_on = datetime.now()
        self.updated_on = datetime.now()

    def json(self):
        if self is not None:
            return {'id': self.id, 'coupon_name': self.name, 'coupon_holder': self.user_id,
                    'description': self.description, 'offer': self.offer,
                    'coupon_code': self.coupon_code, 'brand': Brand.get_by_id(self.brand_id),
                    'qr/bar code': self.coupon_key, 'user': User.get_user_by_id(self.user_id),
                    'expiry_date': self.expiry_date, 'price': self.sale_price}
        else:
            raise NotFoundException('the given data is not present in database')

    @staticmethod
    def add_coupon(user_id, name, description, offer, coupon_code, brand_name, unique_number, expiry_date,
                   price):
        brand_by_name = Brand.json(Brand.query.filter_by(name=brand_name, is_active=True).first())
        print(brand_by_name)
        coupon = Coupon(user_id, name, description, offer, coupon_code, price, brand_by_name['id'],
                        unique_number, expiry_date)
        coupon.created_by = pickle.dumps(User.get_user_by_id(user_id))
        coupon.updated_by = coupon.created_by
        if brand_by_name is not None:
            db.session.add(coupon)
            db.session.commit()

    @staticmethod
    def get_all_coupons():
        return [Coupon.json(coupon) for coupon in Coupon.query.all()]

    @staticmethod
    def get_coupon_by_brand(brand_name):
        brand_by_name = Brand.get_by_brand(brand_name)
        if brand_by_name is not None:
            return [Coupon.json(coupon) for coupon in Coupon.query.filter_by(brand_id=brand_by_name['id']).all()]

    @staticmethod
    def get_coupon_by_brand_type(brand_type):
        brand_by_type = Brand.get_by_type(brand_type)
        a = []
        for brand in brand_by_type:
            if brand is not None:
                a.extend([Coupon.json(coupon) for coupon in Coupon.query.filter_by(brand_id=brand['id']).all()])
        return a

    @staticmethod
    def get_coupon_by_id(coupon_id):
        coupon_by_id = Coupon.json(Coupon.query.filter_by(id=coupon_id).first())
        if coupon_by_id is not None:
            return coupon_by_id

    @staticmethod
    def get_coupon_by_user(user_name):
        brand_by_user = User.get_user_by_username(user_name)

        coupon_by_user_id = Coupon.json(Coupon.query.filter_by(user_id=brand_by_user['id']).first())
        if coupon_by_user_id is not None:
            return coupon_by_user_id

    @staticmethod
    def buy_coupon(coupon_id, buyer_id):
        payment_status = Payment.pay().lower()
        if payment_status == 'successful':
            coupon_by_id = Coupon.query.filter_by(id=coupon_id).first()
            seller_id = coupon_by_id.user_id
            coupon_price = coupon_by_id.sale_price
            coupon_by_id.user_id = buyer_id
            coupon_by_id.updated_on = datetime.now()
            db.session.commit()
            status = 1
            Transaction.create_transaction(status, coupon_id, buyer_id, seller_id, coupon_price)
        # else:
        #     coupon_by_id = Coupon.query.filter_by(id=coupon_id).first()
        #     coupon_by_id.user_id = buyer_id
        #     coupon_by_id.updated_on = datetime.now()
        #     db.session.commit()
        #     Transaction.create_transaction(status, coupon_id, buyer_id, seller_id, coupon_price)

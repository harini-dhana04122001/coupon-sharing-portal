from datetime import datetime
from flaskr import db


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

    def json(self):
        return {'id': self.id, 'brand_name': self.name,
                'brand_type': self.types}

    @staticmethod
    def add_brand(name, types):
        db.session.add(Brand(name, types))
        db.session.commit()

    @staticmethod
    def get_all_brands():
        return [Brand.json(brand) for brand in Brand.query.filter_by(is_active=True).all()]

    @staticmethod
    def get_by_id(brand_id):
        return Brand.json(Brand.query.filter_by(id=brand_id, is_active=True).first())

    @staticmethod
    def get_by_brand(brand_name):
        return Brand.query.filter_by(name=brand_name, is_active=True).first()

    @staticmethod
    def get_by_type(brand_type):
        return [Brand.json(brand) for brand in Brand.query.filter_by(types=brand_type, is_active=True).all()]

    @staticmethod
    def update_brand(brand_id, key, *args):
        brand = Brand.query.filter_by(id=brand_id, is_active=True).first()
        print(brand)
        if key == 'name':
            brand.name = args[0]
            brand.updated_on = datetime.now()
            db.session.commit()
        elif key == 'type':
            brand.types = args[0]
            brand.updated_on = datetime.now()
            db.session.commit()
        else:
            brand.name = args[0]
            brand.types = args[1]
            brand.updated_on = datetime.now()
            db.session.commit()

    @staticmethod
    def delete_brand(brand_id):
        brand_by_id = Brand.query.filter_by(id=brand_id, is_active=True).first()
        brand_by_id.is_active = False
        db.session.commit()





from datetime import datetime
from flaskr import db
from flaskr.exceptions.notfoundexception import NotFoundException


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

    """
    This method takes in data and display it in form of dictionary

    :return: The result after inserting the data in the dictionary
    :rtype: dict
    :raise: NotFoundException
    """

    def json(self):
        if self is not None:
            return {'id': self.id, 'brand_name': self.name,
                    'brand_type': self.types}
        else:
            raise NotFoundException('the given data is not present in database')

    """
    This method takes in brand details and store them in database.

    :arg name: the argument have name of brand.
    :arg type: the argument have contact of brand.
    """

    @staticmethod
    def add_brand(name, types):
        db.session.add(Brand(name, types))
        db.session.commit()

    """
    This method displays all the brand which is present in database

    :return: The result after getting the data from the database and adding it to list
    :rtype: list(dict)
    """

    @staticmethod
    def get_all_brands():
        return [Brand.json(brand) for brand in Brand.query.filter_by(is_active=True).all()]

    """
    This method displays user with the given brand id

    :return: The result after getting the data from the database with the given brand id
    :rtype: dict
    """

    @staticmethod
    def get_by_id(brand_id):
        return Brand.json(Brand.query.filter_by(id=brand_id, is_active=True).first())

    """
    This method displays user with the given brand name

    :return: The result after getting the data from the database with the given brand name
    :rtype: dict
    """

    @staticmethod
    def get_by_brand(brand_name):
        return Brand.json(Brand.query.filter_by(name=brand_name, is_active=True).first())

    """
    This method displays user with the given brand type

    :return: The result after getting the data from the database with the given brand type
    :rtype: dict
    """

    @staticmethod
    def get_by_type(brand_type):
        return [Brand.json(brand) for brand in Brand.query.filter_by(types=brand_type, is_active=True).all()]

    """
    This method update brand with given brand id
    
    :arg brand_id: the argument have brand id
    :arg key: it have the key with which we can update the brand
    :arg *args: it can have multiple argument.
    """
    @staticmethod
    def update_brand(brand_id, key, *args):
        brand = Brand.query.filter_by(id=brand_id, is_active=True).first()
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

    """
    This method delete brand with the given id

    :arg contact: the argument have id of brand.
    """

    @staticmethod
    def delete_brand(brand_id):
        brand_by_id = Brand.query.filter_by(id=brand_id, is_active=True).first()
        brand_by_id.is_active = False
        db.session.commit()





from datetime import datetime

from flaskr.app import db
from flaskr.exceptions.notfoundexception import NotFoundException
from flaskr.brands.models import Brand

"""
This method takes in data and display it in form of dictionary

:return: The result after inserting the data in the dictionary
:rtype: dict
:raise: NotFoundException
"""


def json(data):
    if data is not None:
        return {'id': data.id, 'brand_name': data.name,
                'brand_type': data.types}
    else:
        raise NotFoundException('the given brand data is not present in database', 'Details Not Found')


"""
This method takes in brand details and store them in database.

:arg name: the argument have name of brand.
:arg type: the argument have contact of brand.
"""


def add_brand(name, types):
    db.session.add(Brand(name, types))
    db.session.commit()


"""
This method displays all the brand which is present in database

:return: The result after getting the data from the database and adding it to list
:rtype: list(dict)
"""


def get_all_brands():
    brand_details = [json(brand) for brand in Brand.query.filter_by(is_active=True).all()]
    if brand_details is None:
        return NotFoundException('There is no data present in the database', 'Details Not Present')
    return


"""
This method displays user with the given brand id

:return: The result after getting the data from the database with the given brand id
:rtype: dict
"""


def get_by_id(brand_id):
    return json(Brand.query.filter_by(id=brand_id, is_active=True).first())


"""
This method displays user with the given brand name

:return: The result after getting the data from the database with the given brand name
:rtype: dict
"""


def get_by_brand(brand_name):
    return json(Brand.query.filter_by(name=brand_name, is_active=True).first())


"""
This method displays user with the given brand type

:return: The result after getting the data from the database with the given brand type
:rtype: dict
"""


def get_by_type(brand_type):
    return [json(brand) for brand in Brand.query.filter_by(types=brand_type, is_active=True).all()]


"""
This method update brand with given brand id

:arg brand_id: the argument have brand id
:arg key: it have the key with which we can update the brand
:arg *args: it can have multiple argument.
"""


def update_brand(brand_id, *args):
    brand = Brand.query.filter_by(id=brand_id, is_active=True).first()
    if args[1] is None:
        brand.name = args[0]
        brand.updated_on = datetime.now()
        db.session.commit()
    elif args[0] is None:
        brand.types = args[1]
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


def delete_brand(brand_id):
    brand_by_id = Brand.query.filter_by(id=brand_id, is_active=True).first()
    brand_by_id.is_active = False
    db.session.commit()


import datetime
import logging

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from flaskr.exceptions.apierror import APIError
from flaskr.exceptions.notfoundexception import NotFoundException

db = SQLAlchemy()


def create_app():
    logging.basicConfig(filename='record.log', format='%(asctime)s %(levelname)s %(name)s : %(message)s ',
                        level=logging.ERROR)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ccfe06a09c594b0b313604b6614fa7434ad7f66ba4c7647559360092bb1de213'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:harini04121@localhost/miniproject'
    db.init_app(app)
    from flaskr.brands.controller import display as brands_display
    from flaskr.coupons.controller import display as coupons_display
    from flaskr.users.controller import display as users_display
    from flaskr.transactions.controller import display as transaction_display
    from flaskr.auth.auth import auth_

    app.register_blueprint(brands_display, name='brands_display', url_prefix='/brand')
    app.register_blueprint(coupons_display, name='coupons_display', url_prefix='/coupon')
    app.register_blueprint(users_display, name='users_display', url_prefix='/user')
    app.register_blueprint(transaction_display, name='transaction_display', url_prefix='/transaction')
    app.register_blueprint(auth_, url_prefix='/auth/')

    @app.errorhandler(APIError)
    def handle_exception(err):
        """Return custom JSON when APIError or its children are raised"""

        response = {"error": err.description, "status code": err.code, "message": "",
                    "timestamp": datetime.datetime.now()}
        if len(err.args) > 0:
            response["message"] = err.args[0]
        # Add some logging so that we can monitor different types of errors
        logging.error(f'{err.description} - {request.url_root} - {request.get_data()}: {response["message"]}')
        return jsonify(response), err.code

    with app.app_context():
        db.create_all()
        return app

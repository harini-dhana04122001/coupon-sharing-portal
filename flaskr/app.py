import datetime
import logging
import uuid

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    logging.basicConfig(filename='error-record.log', format='%(asctime)s %(levelname)s %(name)s : %(message)s ',
                        level=logging.ERROR)
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ccfe06a09c594b0b313604b6614fa7434ad7f66ba4c7647559360092bb1de213'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:harini04121@localhost/online_coupon'
    db.init_app(app)
    migrate.init_app(app, db)
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

    @app.errorhandler(Exception)
    def handle_exception(err):
        """Return custom JSON when APIError are raised"""
        err_uuid = uuid.uuid4()
        error_code = 500
        response = {"error": err.__class__.__name__, "status code": error_code, "message": "",
                    "timestamp": datetime.datetime.now(), "error uuid": err_uuid}
        if len(err.args) > 1:
            response["message"] = err.args[0]
            response["error"] = err.description
            response["status code"] = err.code
            error_code = err.code
            logging.error(
                f'{err_uuid} --- {err.description} - {request.url} : {response["message"]}')
        elif 0 < len(err.args) < 2:
            response["message"] = err.args[0]
            logging.error(
                f'{err_uuid} --- {err.__class__.__name__} - {request.url}: {response["message"]}')
            error_code = error_code

        # Adding some logging so that we can monitor different types of errors

        return jsonify(response), error_code

    with app.app_context():
        db.create_all()
        return app

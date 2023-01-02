from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ccfe06a09c594b0b313604b6614fa7434ad7f66ba4c7647559360092bb1de213'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:harini04121@localhost/miniproject'
    db.init_app(app)
    from flaskr.views import display
    from .auth import auth_

    app.register_blueprint(display, url_prefix='/')
    app.register_blueprint(auth_, url_prefix='/auth/')
    with app.app_context():
        db.create_all()
        return app


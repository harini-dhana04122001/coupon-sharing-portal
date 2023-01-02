from flask_sqlalchemy import SQLAlchemy
from flaskr import db
from flaskr import create_app

app = create_app()


if __name__ == '__main__':
    app.run(host='localhost',
            port='8080',
            debug=True)

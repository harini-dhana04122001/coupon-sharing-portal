from flask import Blueprint

auth_ = Blueprint('auth', __name__)


@auth_.route('home')
def new():
    return 'access granted'

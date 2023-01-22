import re
from datetime import datetime


def validate_number(number):
    if not re.match('^\\+?\\d{1,4}?[-.\\s]?\\(?\\d{1,3}?\\)?[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,4}[-.\\s]?\\d{1,9}$', number):
        return False
    else:
        return True
    # if not valid_number:
    #     return False
    # else:
    #     return True


def validate_date(date):
    valid_date = re.match('^[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}$', date)
    return valid_date


def validate_name(name):
    valid_name = re.match('^[A-Za-z0-9]{1,30}$', name)
    if not valid_name:
        return False
    else:
        return True


def calculate_age(date_of_birth):
    today_date = datetime.today()
    str_dob = date_of_birth.strftime("%d-%m-%Y")
    age = today_date.year - int(str_dob[6:10]) - (
            (today_date.month, today_date.day) < (int(str_dob[3:5]), int(str_dob[0:2])))
    return age


def validate_password(password):
    if not re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@_$%^&*-]).{6,30}$',password):
        return False
    else:
        return True

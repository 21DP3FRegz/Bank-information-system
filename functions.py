from datetime import datetime, timedelta
import bcrypt


def is_in_period(datetime_string, delta):
    datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d")
    timedelta_object = datetime.today() - datetime_object
    comparison_datetime = datetime.today() - delta
    return timedelta_object < comparison_datetime


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')

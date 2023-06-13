from datetime import datetime, timedelta

def is_in_period(datetime_string, delta):
    datetime_object = datetime.strptime(datetime_string, "%Y-%m-%d")
    timedelta_object = datetime.today() - datetime_object
    comparison_datetime = datetime.today() - delta
    return timedelta_object < comparison_datetime
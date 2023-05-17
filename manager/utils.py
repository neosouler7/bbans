import os
import json
from datetime import datetime, timedelta

DATE_FORMAT_YmdHMS = "%Y-%m-%d %H:%M:%S"


def get_current_time(date_format=None, day_delta=None):
    today = datetime.utcnow() + timedelta(hours=9)

    if day_delta is not None:
        today += timedelta(days=day_delta)
    
    if date_format is None:
        return today
    return today.strftime(date_format)

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%Y%m%d")
        return True
    except ValueError:
        return False
    
def to_date_dot(date_string):
    year, month, day = date_string[:4], date_string[4:6], date_string[6:]
    return f"{year}.{month}.{day}"

def read_config():
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../config.json', 'r') as _config_file:
        return json.load(_config_file)
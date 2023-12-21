import pytz
from datetime import datetime


def get_tashkent_time():
    tz = pytz.timezone('Asia/Tashkent')
    return datetime.now(tz)

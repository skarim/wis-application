# coding=utf-8
import pytz
import datetime

from application.settings import TIME_ZONE


def localize(date, time):
    # shift datetimes for storing
    dt_str = '%s %s' % (date.strip(), time.strip())
    local_tz = pytz.timezone(TIME_ZONE)
    dt = datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
    dt = local_tz.localize(dt).astimezone(
        pytz.utc
    ).replace(tzinfo=None)
    return dt


def get_diff_from_now(date):
    # get the delta between a datetime and current time (in hours)
    local_tz = pytz.timezone(TIME_ZONE)
    current = datetime.datetime.now()
    current = local_tz.localize(current).astimezone(
        pytz.utc
    ).replace(tzinfo=None)
    delta = (date.replace(tzinfo=None) - current)
    hours_delta = (delta.days*24) + delta.seconds//3600
    return hours_delta

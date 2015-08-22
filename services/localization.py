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

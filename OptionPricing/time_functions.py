from datetime import datetime, date, timedelta
from time import mktime


def to_unix_time(datetime_str):
    try:
        dt_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        unix_time_ms = int(mktime(dt_obj.timetuple()) * 1000)

        return str(unix_time_ms)

    except ValueError:
        return "Invalid datetime format. Please provide a datetime in the format '%Y-%m-%d %H:%M:%S'."


def from_unix_time(unix_time_str):
    try:
        unix_time_ms = int(unix_time_str)
        dt_obj = datetime.fromtimestamp(unix_time_ms / 1000.0)
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %H:%M:%S')

        return formatted_datetime

    except ValueError:
        return "Invalid Unix timestamp format. Please provide a numerical Unix timestamp."



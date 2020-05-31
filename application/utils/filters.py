from application import app
from datetime import datetime as dt


@app.template_filter("datetime")
def format_datetime(value):
    if type(value) is str:
        return dt.strptime(value, "%Y-%m-%d %H:%M:%S.%f").strftime("%-d.%-m.%Y %H:%M")
    else:
        return value.strftime("%-d.%-m.%Y %H:%M")

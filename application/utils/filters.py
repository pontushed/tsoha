from application import app
from datetime import datetime as dt


@app.template_filter("datetime")
def format_datetime(value):

    return dt.strptime(value, "%Y-%m-%d %H:%M:%S.%f").strftime("%-d.%-m.%Y %H:%M")

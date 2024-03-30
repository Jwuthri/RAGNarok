from datetime import datetime


def readable_today_date():
    return datetime.now().strftime("%d %B %Y")

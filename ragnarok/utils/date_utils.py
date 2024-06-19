from datetime import datetime


def readable_today_date():
    """
    The function `readable_today_date` returns the current date in a readable format with day, month, and year.
    """
    return datetime.now().strftime("%d %B %Y")

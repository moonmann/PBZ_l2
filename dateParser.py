from datetime import datetime


def parse_date(date_str):
    try:
        date_object = datetime.strptime(date_str, '%d.%m.%Y')
        return True
    except ValueError:
        return False

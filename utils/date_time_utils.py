from datetime import datetime, timedelta


def get_flyers_wednesday_start_date() -> datetime:
    today_weekday = datetime.today().weekday()
    current_date = datetime.today()
    # Monday or Tuesday => return to the last Wednesday
    if today_weekday <= 1:
        return current_date - timedelta(days=datetime.today().weekday() + 5)
    # Otherwise, return the current Wednesday
    return current_date - timedelta(days=datetime.today().weekday() - 2)


def get_flyers_wednesday_end_date() -> datetime:
    return get_flyers_wednesday_start_date() + timedelta(days=7)


def to_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def to_datetime(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")

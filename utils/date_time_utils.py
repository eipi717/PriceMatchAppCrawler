from datetime import datetime, timedelta


def get_flyers_start_date_thursday() -> datetime:
    today_weekday = datetime.today().weekday()
    current_date = datetime.today()
    # Monday or Tuesday => return to the last Thursday
    if today_weekday <= 2:
        return current_date - timedelta(days=datetime.today().weekday() + 4)
    # Otherwise, return the current Thursday
    return current_date - timedelta(days=datetime.today().weekday() - 3)


def get_flyers_end_date_wednesday() -> datetime:
    return get_flyers_start_date_thursday() + timedelta(days=6)


def to_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def to_datetime(date: datetime) -> str:
    return date.strftime("%Y-%m-%d %H:%M:%S")

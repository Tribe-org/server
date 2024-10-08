from datetime import datetime


def check_age(birthday: datetime, age: int):
    today = datetime.today()

    diff = today - birthday

    # 윤년을 고려해 계산해야해서 365.25일을 곱함
    required_days = age * 365.25

    return diff.days >= required_days

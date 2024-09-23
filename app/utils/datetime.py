from datetime import datetime


def create_timestamptz(birthyear: int, birthday: str) -> datetime:
    # birthyear와 birthday 문자열을 결합하여 "YYYY-MM-DD" 형식의 날짜 문자열 생성
    full_birthday = f"{birthyear}-{birthday}"

    # 문자열을 datetime 객체로 변환 (Supabase의 timestamptz에 맞는 UTC 시간)
    birthday_datetime = datetime.strptime(full_birthday, "%Y-%m-%d")

    return birthday_datetime

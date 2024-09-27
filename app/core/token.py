import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Token:
    ALGORITHM = "HS256"

    def __init__(self):
        env = os.getenv("ENV")

        # 개발 환경
        if env == "DEV":
            self._ACCESS_TOKEN_DURATION = timedelta(minutes=30)
            self._REFRESH_TOKEN_DURATION = timedelta(days=1)
        # 운영 환경
        elif env == "PROD":
            self._ACCESS_TOKEN_DURATION = timedelta(days=1)
            self._REFRESH_TOKEN_DURATION = timedelta(days=7)

    @property
    def ACCESS_TOKEN_DURATION(self):
        return self._ACCESS_TOKEN_DURATION

    @property
    def REFRESH_TOKEN_DURATION(self):
        return self._REFRESH_TOKEN_DURATION

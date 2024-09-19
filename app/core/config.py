import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL")
    NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
    NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
    NAVER_REDIRECT_URL = os.getenv("NAVER_REDIRECT_URL")

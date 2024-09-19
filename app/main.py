import os
from enum import Enum

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.core import database_bootstrap
from app.routers.router import main_router

load_dotenv()

# 데이터베이스 설정
database_bootstrap()


class Environment(str, Enum):
    DEV = "DEV"
    PROD = "PROD"


env = os.getenv("ENV")

if env == Environment.DEV:
    # 개발 환경일 때는 구글 로그인 HTTP에서 가능하도록 설정
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = FastAPI()

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URL = os.getenv("KAKAO_REDIRECT_URL")
GOOGLE_REDIRECT_URL = os.getenv("GOOGLE_REDIRECT_URL")

# CORS 설정 추가
origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SessionMiddleware, secret_key=APP_SECRET_KEY)

app.include_router(main_router, prefix="/v1")


@app.get("/")
async def root():
    return {"message": "Hello World"}

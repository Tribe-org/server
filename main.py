from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from urllib.parse import urlencode
from pydantic import BaseModel
import httpx
import os

load_dotenv()

app = FastAPI()

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_REDIRECT_URL = os.getenv("KAKAO_REDIRECT_URL")

# CORS 설정 추가
origins = ["http://localhost:8000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/auth/kakao")
async def login_kakao():
    kakao_auth_url = "https://kauth.kakao.com/oauth/authorize"
    params = {
        "response_type": "code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URL,
    }

    query_string = urlencode(params)

    url = f"{kakao_auth_url}?{query_string}"

    print(url)
    return RedirectResponse(url)


class KakaoCallbackModel(BaseModel):
    code: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


@app.post("/auth/kakao/callback")
async def login_kakao_token(model: KakaoCallbackModel):
    if not model.code:
        raise HTTPException(status_code=400, detail="code is not a string")

    url = "https://kauth.kakao.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URL,
        "client_secret": KAKAO_CLIENT_SECRET,
        "code": model.code,
    }

    async with httpx.AsyncClient() as client:
        httpx_response = await client.post(url, headers=headers, data=data)
        response = httpx_response.json()

        # 에러 검사
        if response.get("error"):
            raise HTTPException(status_code=500, detail="에러 나중에 처리해야 함")

    return TokenModel(
        access_token=response.get("access_token"),
        refresh_token=response.get("refresh_token"),
    )

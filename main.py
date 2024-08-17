import os
from urllib.parse import urlencode

import google_auth_oauthlib.flow
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

load_dotenv()

app = FastAPI()

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


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/auth/kakao/start")
async def auth_kakao_start():
    kakao_auth_url = "https://kauth.kakao.com/oauth/authorize"

    params = {
        "response_type": "code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URL,
    }

    query_string = urlencode(params)

    url = f"{kakao_auth_url}?{query_string}"

    return RedirectResponse(url)


@app.get("/auth/kakao/callback")
async def auth_kakao_callback(code: str):
    if not code:
        raise HTTPException(status_code=400, detail="code is not a string")

    url = "https://kauth.kakao.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {
        "grant_type": "authorization_code",
        "client_id": KAKAO_CLIENT_ID,
        "redirect_uri": KAKAO_REDIRECT_URL,
        "client_secret": KAKAO_CLIENT_SECRET,
        "code": code,
    }

    async with httpx.AsyncClient() as client:
        httpx_response = await client.post(url, headers=headers, data=data)
        response = httpx_response.json()

        # 에러 검사
        if response.get("error"):
            raise HTTPException(status_code=500, detail="에러 나중에 처리해야 함")

    return await auth_kakao_user_me(response.get("access_token"))


async def auth_kakao_user_me(access_token: str):
    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        "Authorization": f"Bearer {access_token}",
    }
    params = {"secure_resource": True}

    async with httpx.AsyncClient() as client:
        httpx_response = await client.post(url, headers=headers, params=params)
        response = httpx_response.json()

    return response


@app.get("/auth/google/start")
async def auth_google_start():
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
    )

    flow.redirect_uri = GOOGLE_REDIRECT_URL

    authorization_url, state = flow.authorization_url(
        access_type="offline", include_granted_scopes="true", prompt="consent"
    )

    return RedirectResponse(url=authorization_url)


@app.get("/auth/google/callback")
async def auth_google_callback(
    state: str, error: str | None = None, code: str | None = None
):
    if error == "access_denied":
        raise HTTPException(status_code=500, detail=error)

    if code is None:
        raise HTTPException(status_code=500, detail="code does not exist.")

    # print(request.url)
    return RedirectResponse(url="http://localhost:3000")

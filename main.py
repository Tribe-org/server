import os
from enum import Enum
from urllib.parse import urlencode

import google_auth_oauthlib.flow
import googleapiclient.discovery
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()


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
async def auth_google_start(request: Request):
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

    request.session["state"] = state

    return RedirectResponse(url=authorization_url)


@app.get("/auth/google/callback")
async def auth_google_callback(request: Request):
    state = request.query_params.get("state")
    error = request.query_params.get("error")
    code = request.query_params.get("code")

    # 저장한 state와 비교해 맞지 않으면 허용하지 않음
    if state != request.session["state"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    # 사용자가 로그인 취소한 경우
    if error == "access_denied":
        raise HTTPException(status_code=500, detail=error)

    if code is None:
        raise HTTPException(status_code=500, detail="code does not exist.")

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secret.json",
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
        ],
        state=state,
    )

    flow.redirect_uri = GOOGLE_REDIRECT_URL

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)

    return await auth_google_user_me(flow.credentials)


async def auth_google_user_me(credentials):
    service = googleapiclient.discovery.build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()

    # 유저 정보 출력 (로그에 출력)
    print(f"User Info: {user_info}")

    return user_info

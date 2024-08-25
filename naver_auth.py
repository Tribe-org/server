import os
import secrets
from urllib.parse import urlencode

import httpx
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

load_dotenv()

router = APIRouter()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_REDIRECT_URL = os.getenv("NAVER_REDIRECT_URL")


def generate_state():
    return secrets.token_urlsafe(16)


@router.get("/start")
async def auth_naver_start():
    naver_auth_url = "https://nid.naver.com/oauth2.0/authorize"
    state = generate_state()
    params = {
        "response_type": "code",
        "client_id": NAVER_CLIENT_ID,
        "redirect_uri": NAVER_REDIRECT_URL,
        "state": state,
    }

    query_string = urlencode(params)
    url = f"{naver_auth_url}?{query_string}"

    return RedirectResponse(url)


@router.get("/callback")
async def auth_naver_callback(code: str, state: str):
    if not code:
        raise HTTPException(status_code=400, detail="code is not provided")

    url = "https://nid.naver.com/oauth2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"}
    data = {
        "grant_type": "authorization_code",
        "client_id": NAVER_CLIENT_ID,
        "client_secret": NAVER_CLIENT_SECRET,
        "redirect_uri": NAVER_REDIRECT_URL,
        "code": code,
        "state": state,
    }

    async with httpx.AsyncClient() as client:
        httpx_response = await client.post(url, headers=headers, data=data)
        response = httpx_response.json()

        if response.get("error"):
            raise HTTPException(status_code=500, detail="에러 나중에 처리해야 함")

    return await auth_naver_user_me(response.get("access_token"))


async def auth_naver_user_me(access_token: str):
    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    url = "https://openapi.naver.com/v1/nid/me"
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    async with httpx.AsyncClient() as client:
        httpx_response = await client.get(url, headers=headers)
        response = httpx_response.json()

    return response

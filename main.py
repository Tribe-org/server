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

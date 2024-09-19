from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

from app.services import NaverService

auth_router = APIRouter()


naver_service = NaverService()


@auth_router.get("/start")
def auth_start():
    url = naver_service.auth_start()
    return RedirectResponse(url)


@auth_router.get("/callback")
async def auth_callback(code: str, state: str):
    if not code:
        raise HTTPException(status_code=400, detail="code is not provided")
    if not state:
        raise HTTPException(status_code=400, detail="state is not provided")

    response = await naver_service.auth_callback(code, state)

    access_token = response.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    return await naver_service.user_me(access_token)

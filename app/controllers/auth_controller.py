from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core import get_db
from app.services import NaverService, UserService

auth_router = APIRouter()


naver_service = NaverService()
user_service = UserService()


@auth_router.get("/start")
def auth_start():
    url = naver_service.auth_start()
    return RedirectResponse(url)


@auth_router.get("/callback")
async def auth_callback(code: str, state: str, db: Session = Depends(get_db)):
    if not code:
        raise HTTPException(status_code=400, detail="code is not provided")
    if not state:
        raise HTTPException(status_code=400, detail="state is not provided")

    response = await naver_service.auth_callback(code, state)

    access_token = response.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    # 네이버 회원정보 가져오기
    user = await naver_service.user_me(access_token)

    print(f"유저?? {user}")
    # 회원가입 진행
    user_service.sign_up(db, user)

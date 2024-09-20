from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core import get_db
from app.dtos import naver
from app.services import NaverService, UserService

auth_router = APIRouter()

naver_service = NaverService()
user_service = UserService()


@auth_router.get("/start")
def auth_start():
    url = naver_service.auth_start()
    return RedirectResponse(url)


@auth_router.get("/callback")
async def auth_callback(
    code: str, state: str, request: Request, db: Session = Depends(get_db)
):
    if not code:
        raise HTTPException(status_code=400, detail="code is not provided")
    if not state:
        raise HTTPException(status_code=400, detail="state is not provided")

    response = await naver_service.auth_callback(code, state)

    access_token = response.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    # 네이버 회원정보 가져오기
    naver_user_info = await naver_service.user_me(access_token)

    # 회원 정보를 조회
    user_exist = user_service.user_exists(db, email=naver_user_info.email)

    # TODO 회원 정보가 있으면, 로그인 처리

    # 회원 정보가 없으면 세션에 로그인 정보 저장 후, 회원가입 페이지로 리디렉션
    if not user_exist:
        request.session[code] = naver_user_info.model_dump()

        params = {"code": code}
        query_string = urlencode(params)
        url = f"/signup?{query_string}"

        return RedirectResponse(url, status_code=301)


@auth_router.post("/naver/user_info")
def get_naver_user_info(code: str, request: Request):
    naver_user_info = request.session.get(code)

    if not naver_user_info:
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    return naver.NaverUserInfoDTO(**naver_user_info)

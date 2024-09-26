from urllib.parse import urlencode

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core import get_db
from app.dtos import naver
from app.services import AuthService, NaverService, UserService

auth_router = APIRouter()

auth_service = AuthService()
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
    if user_exist:
        access_token, refresh_token = auth_service.sign_in(naver_user_info, db)

        params = {"access_token": access_token}
        query_string = urlencode(params)
        url = f"http://localhost:3000/login?{query_string}"

        response = RedirectResponse(url, status_code=301)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
        )

        return response

    # 회원 정보가 없으면 세션에 로그인 정보 저장 후, 회원가입 페이지로 리디렉션
    if not user_exist:
        # 네이버 회원 정보를 세션에 저장
        request.session[code] = naver_user_info.model_dump()

        params = {"code": code}
        query_string = urlencode(params)
        url = f"http://localhost:3000/signup?{query_string}"

        return RedirectResponse(url, status_code=301)


@auth_router.post("/naver/user_info")
def get_naver_user_info(dto: naver.NaverUserInfoWithCodeDTO, request: Request):
    code = dto.code

    if not code:
        raise HTTPException(status_code=400, detail="code가 필요합니다.")

    naver_user_info: naver.NaverUserDTO = request.session.get(code)

    if not naver_user_info:
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    return naver.NaverUserInfoWithEmailAndNameDTO(**naver_user_info)


@auth_router.post("/sign-up")
def sign_up(
    request: Request,
    code: str = Form(...),
    email: str = Form(...),
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    naver_user_info: naver.NaverUserDTO = request.session.get(code)

    if not naver_user_info:
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    # 회원가입 진행
    new_tribe_user = user_service.sign_up(db, naver.NaverUserDTO(**naver_user_info))

    # 회원가입이 끝났으면 세션 초기화
    request.session.clear()

    return new_tribe_user

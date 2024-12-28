from datetime import datetime

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response

from app.core import Config
from app.dtos import naver
from app.services import AuthService, NaverService, TokenService, UserService
from app.utils import check_age, make_url

auth_router = APIRouter(tags=["auth"])

auth_service = AuthService()
naver_service = NaverService()
user_service = UserService()
token_service = TokenService()

@auth_router.get("/start")
def auth_start():
    # 로그인 시작 시 네이버 인증 URL 생성 및 리다이렉트
    url = naver_service.auth_start()
    return RedirectResponse(url)

@auth_router.get("/callback")
async def auth_callback(code: str, state: str, request: Request):

    if not code:
        raise HTTPException(status_code=400, detail="code가 제공되지 않았습니다.")

    if not state:
        raise HTTPException(status_code=400, detail="state가 제공되지 않았습니다.")

    # 네이버 인증 처리 후 액세스 토큰을 가져오기
    response = await naver_service.auth_callback(code, state)
    access_token = response.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="access_token이 필요합니다.")

    generate_url = make_url(Config.CLIENT_URL)

    # 네이버 사용자 정보를 가져오기
    naver_user_info = await naver_service.user_me(access_token)
    birthday = datetime.strptime(
        f"{naver_user_info.birthyear}-{naver_user_info.birthday}", "%Y-%m-%d"
    )

    # 사용자가 14세 미만인지 확인 후, 네이버 연동을 해제
    if not check_age(birthday=birthday, age=14):
        delete_result = await naver_service.delete_token(access_token)

        if delete_result:
            params = {"message": "14세 미만은 가입할 수 없습니다."}
            url = generate_url("/login", params=params)

            response = RedirectResponse(url, status_code=301)
            return response

    # 사용자 이메일로 회원 정보 확인 및 처리
    if user_service.user_exists(email=naver_user_info.email):
        # 사용자 정보가 존재하면 액세스 토큰과 리프레시 토큰을 생성합니다.
        access_token, refresh_token = auth_service.sign_in(naver_user_info)

        params = {"access_token": access_token}
        url = generate_url("/login", params=params)

        response = RedirectResponse(url, status_code=301)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            samesite="lax",
        )
        return response
    else:
        try:
            # 사용자 정보가 존재하지 않으면 회원가입을 처리
            auth_service.sign_up(naver_user_info)
        except Exception as e:
            raise HTTPException(status_code=500, detail="회원가입에 실패했습니다.")

        params = {"access_token": "", "code": code}
        url = generate_url("/login", params=params)

        return RedirectResponse(url, status_code=301)

@auth_router.post("/naver/user_info")
def get_naver_user_info(dto: naver.NaverUserInfoWithCodeDTO, request: Request):
    # 네이버 사용자 정보를 조회
    code = dto.code

    if not code:
        # code가 제공되지 않았을 경우 예외 발생
        raise HTTPException(status_code=400, detail="code가 필요합니다.")

    naver_user_info: naver.NaverUserDTO = request.session.get(code)

    if not naver_user_info:
        # 세션이 만료되었거나 유효하지 않은 경우 예외 발생
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    return naver.NaverUserInfoWithEmailAndNameDTO(**naver_user_info)

@auth_router.post("/sign-up")
def sign_up(request: Request, code: str = Form(...)):
    naver_user_info: naver.NaverUserDTO = request.session.get(code)

    if not naver_user_info:
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    new_tribe_user = auth_service.sign_up(naver_user_info)

    # 회원가입이 완료되면 세션을 초기화
    request.session.clear()

    return new_tribe_user

@auth_router.post("/token/refresh")
def refresh_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 유효하지 않거나 만료되었습니다.",
        )

    new_access_token = auth_service.issue_access_token(refresh_token)
    return {"access_token": new_access_token}

@auth_router.post("/token/validate")
def validate_token(token: str):
    is_valid = auth_service.validate_token(token)

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 유효하지 않거나 만료되었습니다.",
        )
    return Response(status_code=status.HTTP_200_OK)

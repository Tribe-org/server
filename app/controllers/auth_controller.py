from datetime import datetime

from fastapi import APIRouter, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse, Response
from app.core import Config
from app.core.database import session_scope
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
    url = naver_service.auth_start()
    print(f"[DEBUG] Redirecting to URL: {url}")
    return RedirectResponse(url)


@auth_router.get("/callback")
async def auth_callback(code: str, state: str, request: Request):
    print(f"[DEBUG] Callback received with code: {code}, state: {state}")
    if not code:
        print("[ERROR] Code is not provided")
        raise HTTPException(status_code=400, detail="code is not provided")
    if not state:
        print("[ERROR] State is not provided")
        raise HTTPException(status_code=400, detail="state is not provided")

    print("[DEBUG] Calling NaverService auth_callback...")
    response = await naver_service.auth_callback(code, state)
    print(f"[DEBUG] Naver auth response: {response}")

    access_token = response.get("access_token")
    if not access_token:
        print("[ERROR] Access token is missing in the response")
        raise HTTPException(status_code=400, detail="access_token가 필요합니다.")

    print(f"[DEBUG] Access token received: {access_token}")
    generate_url = make_url(Config.CLIENT_URL)
    print(f"[DEBUG] Generated URL: {generate_url}")

    print("[DEBUG] Fetching user information from Naver...")
    naver_user_info = await naver_service.user_me(access_token)
    print(f"[DEBUG] Naver user info: {naver_user_info}")

    birthday = datetime.strptime(
        f"{naver_user_info.birthyear}-{naver_user_info.birthday}", "%Y-%m-%d"
    )
    print(f"[DEBUG] User birthday: {birthday}")

    # 사용자가 14세 미만인지 확인
    if not check_age(birthday=birthday, age=14):
        print("[DEBUG] User is under 14 years old, revoking token...")
        delete_result = await naver_service.delete_token(access_token)
        if delete_result:
            print("[DEBUG] Token revoked successfully")
            params = {"message": "14세 미만은 가입할 수 없습니다."}
            url = generate_url("login", params={"access_token": "", "code": code})
            print(f"[DEBUG] Redirecting to: {url}")
            return RedirectResponse(url, status_code=301)

    print("[DEBUG] Checking if user exists in the database...")
    with session_scope() as session:
        user_exist = user_service.user_exists(session, email=naver_user_info.email)
        print(f"[DEBUG] User exists: {user_exist}")

        if user_exist:
            print("[DEBUG] Signing in the user...")
            access_token, refresh_token = auth_service.sign_in(naver_user_info, session)

            params = {"access_token": access_token}
            url = generate_url("login", params=params)
            print(f"[DEBUG] Redirecting to: {url}")

            response = RedirectResponse(url, status_code=301)
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                samesite="lax",
            )
            return response
        else:
            print("[DEBUG] User does not exist, redirecting to sign-up...")
            request.session[code] = naver_user_info.model_dump()

            params = {"access_token": "", "code": code}
            url = generate_url("login", params=params)
            print(f"[DEBUG] Redirecting to: {url}")

            return RedirectResponse(url, status_code=301)


@auth_router.post("/naver/user_info")
def get_naver_user_info(dto: naver.NaverUserInfoWithCodeDTO, request: Request):
    code = dto.code
    print(f"[DEBUG] Received code: {code}")

    if not code:
        print("[ERROR] Code is missing")
        raise HTTPException(status_code=400, detail="code가 필요합니다.")

    naver_user_info: naver.NaverUserDTO = request.session.get(code)
    print(f"[DEBUG] Naver user info from session: {naver_user_info}")

    if not naver_user_info:
        print("[ERROR] Session is expired or invalid")
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    return naver.NaverUserInfoWithEmailAndNameDTO(**naver_user_info)


@auth_router.post("/sign-up")
def sign_up(request: Request, code: str = Form(...)):
    print(f"[DEBUG] Sign-up received with code: {code}")
    naver_user_info = request.session.get(code)
    print(f"[DEBUG] Naver user info from session: {naver_user_info}")

    if not naver_user_info:
        print("[ERROR] Session is expired or invalid")
        raise HTTPException(
            status_code=400, detail="세션이 만료되었거나 유효하지 않습니다."
        )

    with session_scope() as session:
        print("[DEBUG] Signing up user...")
        new_tribe_user = auth_service.sign_up(
            session, naver.NaverUserDTO(**naver_user_info)
        )
        print(f"[DEBUG] New user created: {new_tribe_user}")

        print("[DEBUG] Clearing session...")
        request.session.clear()

    return new_tribe_user


@auth_router.post("/token/refresh")
def refresh_token(request: Request):
    print("[DEBUG] Refresh token endpoint called")
    refresh_token = request.cookies.get("refresh_token")
    print(f"[DEBUG] Refresh token from cookies: {refresh_token}")

    if not refresh_token:
        print("[ERROR] Refresh token is missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token이 필요합니다.",
        )

    with session_scope() as session:
        print("[DEBUG] Validating token...")
        is_expired = auth_service.validate_token(token=refresh_token, db=session)

        if is_expired:
            print("[ERROR] Token is expired or invalid")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 유효하지 않거나 만료되었습니다.",
            )

        new_access_token = auth_service.issue_access_token(refresh_token)
        print(f"[DEBUG] New access token issued: {new_access_token}")

        return {"access_token": new_access_token}


@auth_router.post("/token/validate")
def validate_token(token: str):
    print(f"[DEBUG] Validate token called with token: {token}")

    with session_scope() as session:
        print("[DEBUG] Validating token in the database...")
        is_expired = auth_service.validate_token(token=token, db=session)

        if is_expired:
            print("[ERROR] Token is expired or invalid")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 유효하지 않거나 만료되었습니다.",
            )

        print("[DEBUG] Token is valid")
        return Response(status_code=status.HTTP_200_OK)

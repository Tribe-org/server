from datetime import timedelta

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core import Config, EnvTypes
from app.dtos import auth, naver
from app.repositories import AuthRepository
from app.utils import create_jwt_token, decode_token, is_token_expired

ALGORITHM = "HS256"


class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def sign_in(self, naver_user_info: naver.NaverUserDTO, db: Session):
        """
        로그인 처리 로직
        """

        # 개발 단계
        if Config.ENV is EnvTypes.DEV:
            access_token_duration = timedelta(seconds=10)
            refresh_token_duration = timedelta(days=1)
        elif Config.ENV is EnvTypes.PROD:
            access_token_duration = timedelta(days=1)
            refresh_token_duration = timedelta(days=7)

        data = {"sub": naver_user_info.id}

        access_token = create_jwt_token(data, expires_delta=access_token_duration)
        refresh_token = create_jwt_token(data, expires_delta=refresh_token_duration)

        is_signed_in = self.auth_repository.sign_in(
            uid=naver_user_info.id, refresh_token=refresh_token, db=db
        )

        if not is_signed_in:
            raise HTTPException(status_code=500, detail="로그인을 할 수 없습니다.")

        return access_token, refresh_token

    def issue_access_token(self, refresh_token: str):
        """
        access_token을 발급하는 함수입니다.
        """
        try:
            payload = decode_token(refresh_token)
            uid = payload.get("sub")

            data = {"sub": uid}
            new_access_token = create_jwt_token(
                data, Config.Token.ACCESS_TOKEN_DURATION
            )

            return new_access_token
        except InvalidTokenError:
            raise InvalidTokenError

    def validate_token(self, token: auth.Token, db: Session):
        """
        토큰 값이 유효한지 확인하는 함수입니다.
        """
        try:
            payload = decode_token(token)
            uid: str = payload.get("sub")
        except InvalidTokenError:
            return False

        user_info = self.auth_repository.find_user_by_id(uid, db)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="토큰이 유효하지 않습니다.",
            )

        # refresh_token이 유효한지 확인
        refresh_token = user_info.refresh_token

        try:
            refresh_token_payload = decode_token(refresh_token)
        except InvalidTokenError:
            raise False

        exp = refresh_token_payload.get("exp")

        return is_token_expired(exp)

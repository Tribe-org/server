from datetime import timedelta

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core import Config, EnvTypes
from app.dtos import naver
from app.repositories import AuthRepository
from app.utils import create_jwt_token


class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def sign_in(self, naver_user_info: naver.NaverUserDTO, db: Session):
        """
        로그인 처리 로직
        """

        # 개발 단계
        if Config.ENV is EnvTypes.DEV:
            access_token_duration = timedelta(minutes=30)
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

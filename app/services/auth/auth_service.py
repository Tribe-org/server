from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core import Config, Token
from app.dtos import auth, naver, user
from app.enums import GenderType
from app.models import User
from app.repositories import AuthRepository
from app.utils import create_timestamptz

from .token_service import TokenService

ALGORITHM = "HS256"


class AuthService:
    def __init__(self):
        self.token_service = TokenService()
        self.auth_repository = AuthRepository()
        self.token = Token()

    def sign_in(self, naver_user_info: naver.NaverUserDTO, db: Session):
        """
        로그인 처리 로직
        """

        data = {"sub": naver_user_info.id}

        access_token = self.token_service.create_jwt_token(
            data, expires_delta=self.token.ACCESS_TOKEN_DURATION
        )
        refresh_token = self.token_service.create_jwt_token(
            data, expires_delta=self.token.REFRESH_TOKEN_DURATION
        )

        is_signed_in = self.auth_repository.sign_in(
            uid=naver_user_info.id, refresh_token=refresh_token, db=db
        )

        if not is_signed_in:
            raise HTTPException(status_code=500, detail="로그인을 할 수 없습니다.")

        return access_token, refresh_token

    def sign_up(self, db: Session, naver_user_info: naver.NaverUserDTO):
        uid = naver_user_info.id

        user_info = user.UserDTO(
            uid=uid,
            email=naver_user_info.email,
            name=naver_user_info.name,
            birthday=create_timestamptz(
                birthyear=naver_user_info.birthyear, birthday=naver_user_info.birthday
            ),
            service_agreement=False,
            privacy_consent=False,
            age_consent=False,
            marketing_agreement=False,
            provider="naver",
            gender=GenderType(naver_user_info.gender),
            image_url=None,
            introduction=None,
            refresh_token=None,
            deactivated=False,
        ).model_dump(exclude_unset=True)
        user_model = User(**user_info)

        is_signed_up = self.user_repository.sign_up(db, user_model)

        if not is_signed_up:
            raise HTTPException(status_code=500, detail="회원가입에 실패했습니다.")

        return user_info

    def issue_access_token(self, refresh_token: str):
        """
        access_token을 발급하는 함수입니다.
        """
        try:
            payload = self.token_service.decode_token(refresh_token)
            uid = payload.get("sub")

            data = {"sub": uid}
            new_access_token = self.token_service.create_jwt_token(
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
            payload = self.token_service.decode_token(token)
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
            refresh_token_payload = self.token_service.decode_token(refresh_token)
        except InvalidTokenError:
            raise False

        exp = refresh_token_payload.get("exp")

        return self.token_service.is_token_expired(exp)

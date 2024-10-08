from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError

from app.core import Config
from app.repositories import AuthRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class TokenService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def create_jwt_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()

        expire = datetime.now(timezone.utc) + expires_delta

        to_encode.update(
            {"iat": datetime.now(timezone.utc), "iss": "tribe", "exp": expire}
        )

        encoded_jwt = jwt.encode(
            to_encode, Config.APP_SECRET_KEY, algorithm=Config.Token.ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str):
        return jwt.decode(
            token, Config.APP_SECRET_KEY, algorithms=[Config.Token.ALGORITHM]
        )

    def is_token_expired(self, exp: int):
        """
        토큰 만료 여부를 확인하는 함수입니다.
        """
        current_time = datetime.now(timezone.utc).timestamp()
        return current_time > exp

    def validate_token(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = self.decode_token(token)

            exp = payload.get("exp")

            if self.is_token_expired(exp):
                return HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="토큰이 유효하지 않거나 만료되었습니다.",
                )

            return token
        except InvalidTokenError as e:
            print(f"오류? {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="토큰이 유효하지 않거나 만료되었습니다.",
            )

from datetime import datetime, timedelta, timezone

import jwt

from app.core import Config


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"iat": datetime.now(timezone.utc), "iss": "tribe", "exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, Config.APP_SECRET_KEY, algorithm=Config.Token.ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str):
    return jwt.decode(token, Config.APP_SECRET_KEY, algorithms=[Config.Token.ALGORITHM])


def is_token_expired(exp: int):
    """
    토큰 만료 여부를 확인하는 함수입니다.
    """
    current_time = datetime.now(timezone.utc).timestamp()
    return current_time > exp

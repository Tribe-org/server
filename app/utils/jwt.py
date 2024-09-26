from datetime import datetime, timedelta, timezone

import jwt

from app.core import Config


def create_jwt_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + expires_delta

    to_encode.update({"iat": datetime.now(timezone.utc), "iss": "tribe", "exp": expire})

    encoded_jwt = jwt.encode(to_encode, Config.APP_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

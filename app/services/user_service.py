from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.dtos import naver, user
from app.enums import GenderType
from app.models import User
from app.repositories import UserRepository
from app.utils import create_timestamptz


class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_exists(self, db: Session, email: str):
        return self.user_repository.user_exists_by_email(db, email)

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

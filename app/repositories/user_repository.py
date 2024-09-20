from datetime import datetime

from sqlalchemy.orm import Session

from app.dtos import auth, user
from app.models import User


class UserRepository:
    def user_exists_by_email(self, db: Session, email: str):
        """
        이메일을 가지고 회원 정보를 조회합니다.
        :return: 사용자 존재 여부 (True 또는 False)
        """
        return db.query(User).filter(User.email == email).count() > 0

    def sign_up(self, db: Session, user_info: auth.NaverUserDTO):
        """
        네이버 회원정보를 가지고 트라이브 회원으로 가입합니다.
        :return: 가입한 회원 정보 (user.UserDTO)
        """

        # TODO 나중에 업데이트 필요
        undefined_user_info = {
            "nickname": "닉네임",
            "birthday": datetime.now(),
            "service_agreement": False,  # 기본 동의 처리 예시
            "privacy_consent": False,  # 기본 동의 처리 예시
            "age_consent": False,  # 기본 동의 처리 예시
        }

        new_user = User(
            email=user_info.email,
            name=user_info.name,
            gender=user_info.gender,
            provider="naver",
            **undefined_user_info
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return user.UserDTO.model_validate(new_user)

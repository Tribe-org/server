from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.sql import func

from app.core import Database
from app.enums import GenderType


class User(Database.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=True
    )
    email = Column(String, nullable=True, default="")
    name = Column(String, nullable=True, default="")
    nickname = Column(String, nullable=True)
    birthday = Column(DateTime(timezone=True), nullable=True)
    service_agreement = Column(Boolean, nullable=True, default=False)
    privacy_consent = Column(Boolean, nullable=True, default=False)
    age_consent = Column(Boolean, nullable=True, default=False)
    marketing_agreement = Column(Boolean, nullable=True, default=False)
    provider = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    introduction = Column(Text, nullable=True)
    refresh_token = Column(String, nullable=True)
    gender = Column(Enum(GenderType), nullable=False, default=GenderType.M)

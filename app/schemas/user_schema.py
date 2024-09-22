from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.enums import GenderType


class UserSchema(BaseModel):
    id: int
    uid: str
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    email: Optional[str] = Field(default="")
    name: Optional[str] = Field(default="")
    birthday: Optional[datetime] = None
    service_agreement: bool = False
    privacy_consent: bool = False
    age_consent: bool = False
    marketing_agreement: bool = False
    provider: Optional[str] = None
    image_url: Optional[str] = None
    introduction: Optional[str] = None
    refresh_token: Optional[str] = None
    gender: GenderType = GenderType.M
    deactivated: bool = False

    class Config:
        use_enum_values = True

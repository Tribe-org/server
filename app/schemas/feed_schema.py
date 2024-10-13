from pydantic import BaseModel, Field
from datetime import datetime, timezone
from typing import Optional
from app.enums import FeedType


class FeedSchema(BaseModel):
    id: Optional[int] = None
    content: str
    type: FeedType
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    is_top: bool
    user_id: int
    mission_id: int

    class Config:
        use_enum_values = True

from pydantic import BaseModel

from app.enums import MeetingType


class BadgeSchema(BaseModel):
    id: int
    name: str
    description: str
    icon_url: str
    type: MeetingType

    class Config:
        use_enum_values = True

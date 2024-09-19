from pydantic import BaseModel

from ..enums.enum import MeetingType


class Badge(BaseModel):
    id: int
    name: str
    description: str
    icon_url: str
    type: MeetingType

    class Config:
        use_enum_values = True

from sqlalchemy import VARCHAR, Column, Enum, Integer, Text

from ..core.database import Base
from ..enums.enum import MeetingType


class Badge(Base):
    __tablename__ = "badge"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR, nullable=True)
    description = Column(Text, nullable=True)
    icon_url = Column(VARCHAR, nullable=True)
    type = Column(Enum(MeetingType), default=MeetingType.CONTINUOUS)

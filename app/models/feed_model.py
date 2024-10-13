from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, Text
from sqlalchemy.sql import func

from app.core import Database
from app.enums.enum import FeedType

class Feed(Database.Base):
    __tablename__ = 'feed'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    type = Column(Enum(FeedType), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_top = Column(Boolean, default=False)
    user_id = Column(Integer, nullable=False) # TODO: user_id에 foreign key 제약조건 추가
    mission_id = Column(Integer, nullable=False) # TODO: mission_id에 foreign key 제약조건 추가


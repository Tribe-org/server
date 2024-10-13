from sqlalchemy.orm import Session
from app.models.feed_model import Feed
from app.schemas.feed_schema import FeedSchema
from typing import List, Optional

class FeedRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_feed(self, feed_data: FeedSchema) -> Feed:
        new_feed = Feed(
            content=feed_data.content,
            type=feed_data.type,
            user_id=feed_data.user_id,
            mission_id=feed_data.mission_id,
        )
        self.db.add(new_feed)
        self.db.commit()
        self.db.refresh(new_feed)
        return new_feed

    def get_feeds_by_mission(self, mission_id: int) -> List[Feed]:
        return self.db.query(Feed).filter(Feed.mission_id == mission_id).all()

    def get_feed(self, feed_id: int) -> Optional[Feed]:
        return self.db.query(Feed).filter(Feed.id == feed_id).first()

    def get_all_feeds(self) -> List[Feed]:
        return self.db.query(Feed).all()

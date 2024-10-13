from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import FeedSchema
from app.models import Feed
from app.core import get_db

feed_router = APIRouter()

# 인증 피드 제출
@feed_router.post("/", response_model=FeedSchema)
async def create_feed(feed: FeedSchema, db: Session = Depends(get_db)):
    # TODO: 피드 생성 로직 추가
    new_feed = Feed(**feed.dict())
    try:
        db.add(new_feed)
        db.commit()
        db.refresh(new_feed)
        return new_feed
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="피드 생성 실패: " + str(e))

# 특정 미션의 인증 피드 조회
@feed_router.get("/{mission_id}", response_model=List[FeedSchema])
async def get_feed_by_mission(mission_id: int, db: Session = Depends(get_db)):
    # TODO: 미션 ID에 해당하는 피드 조회 로직 추가
    feeds = db.query(Feed).filter(Feed.mission_id == mission_id).all()
    if not feeds:
        raise HTTPException(status_code=404, detail="해당 미션에 대한 피드가 없습니다.")
    return feeds

# 모든 인증 피드 조회
@feed_router.get("/all", response_model=List[FeedSchema])
async def get_all_feeds(db: Session = Depends(get_db)):
    # TODO: 모든 피드 조회 로직 추가
    all_feeds = db.query(Feed).all()
    return all_feeds

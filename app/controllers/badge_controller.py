from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core import get_db
from app.services import BadgeService

badge_router = APIRouter()


@badge_router.get("/badge/all")
def get_all_badge(db: Session = Depends(get_db)):
    badge_service = BadgeService()
    return BadgeService().get_all_badge(db)

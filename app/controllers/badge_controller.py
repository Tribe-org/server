from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.badge_service import BadgeService

router = APIRouter()


@router.get("/badge/all")
def get_all_badge(db: Session = Depends(get_db)):
    badge_service = BadgeService()
    return BadgeService().get_all_badge(db)

import os
import secrets
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..services.badge_service import BadgeService

router = APIRouter()


@router.get("/badge/all")
def get_all_badge(db: Session = Depends(get_db)):
    badge_service = BadgeService()
    return BadgeService().get_all_badge(db)

from fastapi import APIRouter

from app.controllers import badge_router

from .naver_auth import naver_router

main_router = APIRouter()

main_router.include_router(naver_router, prefix="/auth")
main_router.include_router(badge_router)

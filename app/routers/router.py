from fastapi import APIRouter

from app.controllers import auth_router, badge_router, meeting_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(badge_router)
main_router.include_router(meeting_router)

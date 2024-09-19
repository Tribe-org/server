from fastapi import APIRouter

from app.controllers import auth_router, badge_router

main_router = APIRouter()

main_router.include_router(auth_router, prefix="/auth")
main_router.include_router(badge_router)

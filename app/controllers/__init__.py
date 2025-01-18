from .auth_controller import auth_router
from .badge_controller import badge_router
from .meeting_controller import router as meeting_router

__all__ = ["auth_router", "badge_router", "meeting_router"]

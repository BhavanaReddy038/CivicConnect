from fastapi import APIRouter

from backend.auth.router import router as auth_router
from backend.complaints.router import router as complaints_router
from backend.posts.router import router as posts_router
from backend.ai.router import router as ai_router


api_router = APIRouter()


api_router.include_router(
    auth_router
)

api_router.include_router(
    complaints_router
)

api_router.include_router(
    posts_router
)

api_router.include_router(
    ai_router
)
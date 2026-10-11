from fastapi import APIRouter
from backend.verification.router import router as verification_router
from backend.duplicates.router import router as duplicates_router
from backend.analytics.router import router as analytics_router

api_router = APIRouter(prefix="/api")
api_router.include_router(verification_router)
api_router.include_router(duplicates_router)
api_router.include_router(analytics_router)
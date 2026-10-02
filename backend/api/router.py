from fastapi import APIRouter

from backend.authority.router import router as authority_router
from backend.sla.router import router as sla_router


api_router = APIRouter(
    prefix="/api",
)


api_router.include_router(authority_router)
api_router.include_router(sla_router)
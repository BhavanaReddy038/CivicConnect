from fastapi import FastAPI

from backend.api.router import api_router
from backend.core.config import settings


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    version="1.0.0",
)


app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX,
)


@app.get("/")
def root():
    return {
        "message": "CivicConnect API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
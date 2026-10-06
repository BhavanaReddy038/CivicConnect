from fastapi import FastAPI

from backend.api.router import api_router


app = FastAPI(
    title="CivicConnect API",
    description="AI-Powered Civic Complaint & Accountability Platform",
    version="1.0.0",
)


app.include_router(api_router)


@app.get("/")
def root():
    return {
        "message": "CivicConnect API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
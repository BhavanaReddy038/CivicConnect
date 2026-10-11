from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine
from database.base import Base
from backend.api.router import api_router

# Auto-creates all tables in Supabase PostgreSQL upon server start
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CivicConnect - Community Verification & Analytics API",
    version="1.0.0",
    description="APIs for community verifications, duplicate detection, and civic intelligence"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/health")
def health_check():
    return {"status": "healthy", "module": "community-verification"}
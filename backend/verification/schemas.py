import uuid
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

class IssueConfirmationCreate(BaseModel):
    complaint_id: uuid.UUID
    comments: Optional[str] = None

class ResolutionVerificationCreate(BaseModel):
    complaint_id: uuid.UUID
    status: str = Field(..., pattern="^(FIXED|NOT_FIXED|PARTIALLY_FIXED)$")
    feedback: Optional[str] = None
    evidence_media_urls: Optional[List[str]] = []

class VerificationResponse(BaseModel):
    id: uuid.UUID
    complaint_id: uuid.UUID
    status: str
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
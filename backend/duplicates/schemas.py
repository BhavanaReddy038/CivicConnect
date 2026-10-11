import uuid
from typing import List
from pydantic import BaseModel

class DuplicateCheckRequest(BaseModel):
    title: str
    description: str
    category: str
    latitude: float
    longitude: float

class DuplicateCheckResponse(BaseModel):
    is_potential_duplicate: bool
    potential_duplicate_ids: List[str]
    confidence_score: float
    message: str

class DuplicateMergeRequest(BaseModel):
    primary_complaint_id: uuid.UUID
    duplicate_complaint_ids: List[uuid.UUID]
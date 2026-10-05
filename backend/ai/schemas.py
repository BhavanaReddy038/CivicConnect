from pydantic import BaseModel, Field


class ClassificationRequest(BaseModel):
    text: str = Field(
        min_length=3,
        max_length=10000,
    )


class ClassificationResponse(BaseModel):
    category: str
    severity: str
    confidence: float


class ComplaintAIRequest(BaseModel):
    complaint_id: int
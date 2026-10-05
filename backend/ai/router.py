from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.ai.schemas import (
    ClassificationRequest,
    ClassificationResponse,
    ComplaintAIRequest,
)
from backend.ai import service
from database.database import get_db


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


@router.post(
    "/classify",
    response_model=ClassificationResponse,
)
def classify(
    data: ClassificationRequest,
):

    return service.classify_complaint(
        data
    )


@router.post(
    "/analyze-complaint",
)
def analyze_complaint(
    data: ComplaintAIRequest,
    db: Session = Depends(get_db),
):

    result = service.analyze_complaint(
        db,
        data.complaint_id,
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return result
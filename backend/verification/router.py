import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from backend.verification.schemas import (
    IssueConfirmationCreate,
    ResolutionVerificationCreate,
    VerificationResponse
)
from backend.verification.repository import VerificationRepository

router = APIRouter(prefix="/verification", tags=["Community Verification"])

def get_current_user_id() -> uuid.UUID:
    return uuid.uuid4()

@router.post("/confirm", status_code=status.HTTP_201_CREATED)
def confirm_issue(
    payload: IssueConfirmationCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    confirmation = VerificationRepository.add_confirmation(db, payload.complaint_id, user_id, payload.comments)
    total = VerificationRepository.get_confirmation_count(db, payload.complaint_id)
    return {
        "message": "Issue confirmed by community",
        "confirmation_id": str(confirmation.id),
        "total_confirmations": total
    }

@router.post("/resolve", status_code=status.HTTP_201_CREATED, response_model=VerificationResponse)
def submit_resolution_verification(
    payload: ResolutionVerificationCreate,
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    verification = VerificationRepository.add_resolution_verification(db, user_id, payload.model_dump())
    return verification

@router.get("/{complaint_id}", response_model=List[VerificationResponse])
def get_complaint_verifications(complaint_id: uuid.UUID, db: Session = Depends(get_db)):
    return VerificationRepository.get_verifications(db, complaint_id)
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.database import get_db
from backend.duplicates.schemas import DuplicateCheckRequest, DuplicateCheckResponse, DuplicateMergeRequest
from backend.duplicates.service import DuplicateService
from backend.duplicates.repository import DuplicateRepository

router = APIRouter(prefix="/duplicates", tags=["Duplicate Detection"])

@router.post("/check", response_model=DuplicateCheckResponse)
def check_duplicates(payload: DuplicateCheckRequest):
    return DuplicateService.find_potential_duplicates(payload)

@router.post("/merge", status_code=status.HTTP_200_OK)
def merge_duplicates(payload: DuplicateMergeRequest, db: Session = Depends(get_db)):
    DuplicateRepository.create_duplicate_group(
        db=db,
        primary_complaint_id=payload.primary_complaint_id,
        duplicate_ids=payload.duplicate_complaint_ids
    )
    return {
        "primary_id": str(payload.primary_complaint_id),
        "merged_duplicates": [str(d) for d in payload.duplicate_complaint_ids]
    }
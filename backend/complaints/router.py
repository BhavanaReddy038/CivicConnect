from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.auth.router import get_current_user
from backend.complaints import service
from backend.complaints.schemas import (
    ComplaintCreate,
    ComplaintResponse,
    ComplaintUpdate,
)
from database.database import get_db
from database.models.user import User


router = APIRouter(
    prefix="/complaints",
    tags=["Complaints"],
)


@router.post(
    "",
    response_model=ComplaintResponse,
    status_code=201,
)
def create_complaint(
    data: ComplaintCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.create_complaint(
        db,
        current_user.id,
        data,
    )


@router.get(
    "",
    response_model=list[ComplaintResponse],
)
def list_complaints(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):

    return service.get_complaints(
        db,
        skip,
        limit,
    )


@router.get(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def get_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
):

    return service.get_complaint(
        db,
        complaint_id,
    )


@router.patch(
    "/{complaint_id}",
    response_model=ComplaintResponse,
)
def update_complaint(
    complaint_id: int,
    data: ComplaintUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.update_complaint(
        db,
        complaint_id,
        current_user.id,
        data,
    )


@router.delete(
    "/{complaint_id}",
    status_code=204,
)
def delete_complaint(
    complaint_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service.delete_complaint(
        db,
        complaint_id,
        current_user.id,
    )

    return None
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.complaints import repository
from backend.complaints.schemas import (
    ComplaintCreate,
    ComplaintUpdate,
)
from database.models.complaint import Complaint
from database.models.location import Location


def create_complaint(
    db: Session,
    user_id: int,
    data: ComplaintCreate,
):

    location = None

    if (
        data.latitude is not None
        and data.longitude is not None
    ):
        location = Location(
            address=data.address,
            latitude=data.latitude,
            longitude=data.longitude,
            point=f"SRID=4326;POINT({data.longitude} {data.latitude})",
        )

        db.add(location)
        db.flush()

    complaint = Complaint(
        user_id=user_id,
        category_id=data.category_id,
        location_id=location.id if location else None,
        title=data.title,
        description=data.description,
        affected_people=data.affected_people,
    )

    return repository.create_complaint(
        db,
        complaint,
    )


def get_complaint(
    db: Session,
    complaint_id: int,
):

    complaint = repository.get_complaint(
        db,
        complaint_id,
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    return complaint


def get_complaints(
    db: Session,
    skip: int,
    limit: int,
):
    return repository.get_complaints(
        db,
        skip,
        limit,
    )


def update_complaint(
    db: Session,
    complaint_id: int,
    user_id: int,
    data: ComplaintUpdate,
):

    complaint = get_complaint(
        db,
        complaint_id,
    )

    if complaint.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot modify this complaint",
        )

    update_data = data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(
            complaint,
            key,
            value,
        )

    return repository.update_complaint(
        db,
        complaint,
    )


def delete_complaint(
    db: Session,
    complaint_id: int,
    user_id: int,
):

    complaint = get_complaint(
        db,
        complaint_id,
    )

    if complaint.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this complaint",
        )

    repository.delete_complaint(
        db,
        complaint,
    )
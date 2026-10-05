from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.complaint import Complaint


def create_complaint(
    db: Session,
    complaint: Complaint,
) -> Complaint:

    db.add(complaint)
    db.commit()
    db.refresh(complaint)

    return complaint


def get_complaint(
    db: Session,
    complaint_id: int,
) -> Complaint | None:

    return db.get(
        Complaint,
        complaint_id,
    )


def get_complaints(
    db: Session,
    skip: int = 0,
    limit: int = 20,
):

    return db.scalars(
        select(Complaint)
        .offset(skip)
        .limit(limit)
        .order_by(Complaint.created_at.desc())
    ).all()


def update_complaint(
    db: Session,
    complaint: Complaint,
) -> Complaint:

    db.commit()
    db.refresh(complaint)

    return complaint


def delete_complaint(
    db: Session,
    complaint: Complaint,
):
    db.delete(complaint)
    db.commit()
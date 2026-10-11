import uuid
from typing import List
from sqlalchemy.orm import Session
from database.models.duplicate_group import DuplicateGroup
from database.models.complaint_relationship import ComplaintRelationship

class DuplicateRepository:
    @staticmethod
    def create_duplicate_group(db: Session, primary_complaint_id: uuid.UUID, duplicate_ids: List[uuid.UUID]) -> DuplicateGroup:
        group = DuplicateGroup(primary_complaint_id=primary_complaint_id)
        db.add(group)
        db.flush()

        for dup_id in duplicate_ids:
            rel = ComplaintRelationship(
                group_id=group.id,
                duplicate_complaint_id=dup_id,
                relationship_type="DUPLICATE"
            )
            db.add(rel)

        db.commit()
        db.refresh(group)
        return group
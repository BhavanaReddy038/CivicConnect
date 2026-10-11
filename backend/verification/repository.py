from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from database.models.community_verification import CommunityVerification
from database.models.issue_confirmation import IssueConfirmation
from database.models.resolution_evidence import ResolutionEvidence

class VerificationRepository:
    @staticmethod
    def add_confirmation(db: Session, complaint_id: uuid.UUID, user_id: uuid.UUID, comments: Optional[str] = None) -> IssueConfirmation:
        confirmation = IssueConfirmation(
            complaint_id=complaint_id,
            user_id=user_id,
            comments=comments
        )
        db.add(confirmation)
        db.commit()
        db.refresh(confirmation)
        return confirmation

    @staticmethod
    def get_confirmation_count(db: Session, complaint_id: uuid.UUID) -> int:
        return db.query(IssueConfirmation).filter(IssueConfirmation.complaint_id == complaint_id).count()

    @staticmethod
    def add_resolution_verification(db: Session, user_id: uuid.UUID, data: dict) -> CommunityVerification:
        verification = CommunityVerification(
            complaint_id=data["complaint_id"],
            user_id=user_id,
            status=data["status"],
            feedback=data.get("feedback")
        )
        db.add(verification)
        db.flush()

        for url in (data.get("evidence_media_urls") or []):
            evidence = ResolutionEvidence(
                verification_id=verification.id,
                media_url=url
            )
            db.add(evidence)

        db.commit()
        db.refresh(verification)
        return verification

    @staticmethod
    def get_verifications(db: Session, complaint_id: uuid.UUID) -> List[CommunityVerification]:
        return db.query(CommunityVerification).filter(CommunityVerification.complaint_id == complaint_id).all()
from backend.verification.repository import VerificationRepository
from backend.verification.schemas import ResolutionVerificationCreate, IssueConfirmationCreate

class VerificationService:
    @staticmethod
    def confirm_issue(user_id: str, payload: IssueConfirmationCreate) -> dict:
        record = VerificationRepository.add_confirmation(payload.complaint_id, user_id, payload.comments)
        total = VerificationRepository.get_confirmation_count(payload.complaint_id)
        return {"message": "Issue confirmed by community", "confirmation_id": record["id"], "total_confirmations": total}

    @staticmethod
    def verify_resolution(user_id: str, payload: ResolutionVerificationCreate) -> dict:
        return VerificationRepository.add_resolution_verification(user_id, payload.model_dump())
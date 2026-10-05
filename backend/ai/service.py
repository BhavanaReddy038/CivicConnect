from sqlalchemy.orm import Session

from ai.classification.classifier import classify_text
from backend.ai.schemas import ClassificationRequest


def classify_complaint(
    data: ClassificationRequest,
):

    return classify_text(
        data.text
    )


def analyze_complaint(
    db: Session,
    complaint_id: int,
):

    from database.models.complaint import Complaint
    from database.models.ai_analysis import AIAnalysis

    complaint = db.get(
        Complaint,
        complaint_id,
    )

    if not complaint:
        return None

    result = classify_text(
        complaint.description
    )

    analysis = AIAnalysis(
        complaint_id=complaint.id,
        predicted_category=result.get("category"),
        severity=result.get("severity"),
        confidence=result.get("confidence"),
        severity_score=result.get("confidence"),
    )

    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    return analysis
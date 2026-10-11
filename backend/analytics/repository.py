from typing import Dict, Any
from sqlalchemy.orm import Session
from database.models.analytics_snapshot import AnalyticsSnapshot
from database.models.community_verification import CommunityVerification
from database.models.issue_confirmation import IssueConfirmation

class AnalyticsRepository:
    @staticmethod
    def get_overview_metrics(db: Session) -> Dict[str, Any]:
        total_verified = db.query(CommunityVerification).count()
        total_confirmations = db.query(IssueConfirmation).count()
        latest_snapshot = db.query(AnalyticsSnapshot).order_by(AnalyticsSnapshot.captured_at.desc()).first()

        if latest_snapshot:
            return {
                "total_reported": latest_snapshot.total_reported,
                "total_resolved": latest_snapshot.total_resolved,
                "community_verified_count": total_verified,
                "resolution_rate_percentage": latest_snapshot.resolution_rate,
                "category_breakdown": latest_snapshot.category_distribution
            }

        return {
            "total_reported": total_confirmations,
            "total_resolved": total_verified,
            "community_verified_count": total_verified,
            "resolution_rate_percentage": 0.0,
            "category_breakdown": {}
        }
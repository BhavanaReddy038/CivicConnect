from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Register Person 3 models with SQLAlchemy metadata
from database.models.community_verification import CommunityVerification  # noqa: F401
from database.models.issue_confirmation import IssueConfirmation          # noqa: F401
from database.models.resolution_evidence import ResolutionEvidence        # noqa: F401
from database.models.duplicate_group import DuplicateGroup                # noqa: F401
from database.models.complaint_relationship import ComplaintRelationship  # noqa: F401
from database.models.analytics_snapshot import AnalyticsSnapshot          # noqa: F401
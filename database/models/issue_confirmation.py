import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base

class IssueConfirmation(Base):
    __tablename__ = "issue_confirmations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    complaint_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    comments = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
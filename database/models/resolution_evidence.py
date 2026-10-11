import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base

class ResolutionEvidence(Base):
    __tablename__ = "resolution_evidence"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    verification_id = Column(UUID(as_uuid=True), nullable=False)
    media_url = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
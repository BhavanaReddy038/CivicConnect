import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database.base import Base

class AnalyticsSnapshot(Base):
    __tablename__ = "analytics_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total_reported = Column(Integer, nullable=False)
    total_resolved = Column(Integer, nullable=False)
    verified_resolutions = Column(Integer, nullable=False)
    resolution_rate = Column(Float, nullable=False)
    category_distribution = Column(JSONB, nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow)
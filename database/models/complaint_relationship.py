import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from database.base import Base

class ComplaintRelationship(Base):
    __tablename__ = "complaint_relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(UUID(as_uuid=True), nullable=False)
    duplicate_complaint_id = Column(UUID(as_uuid=True), nullable=False)
    relationship_type = Column(String(50), default="DUPLICATE")
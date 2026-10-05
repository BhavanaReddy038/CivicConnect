import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class ComplaintStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    REJECTED = "REJECTED"


class Complaint(Base):
    __tablename__ = "complaints"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("issue_categories.id"),
        nullable=True,
        index=True,
    )

    location_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    affected_people: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    status: Mapped[ComplaintStatus] = mapped_column(
        Enum(ComplaintStatus),
        default=ComplaintStatus.SUBMITTED,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    user = relationship(
        "User",
        back_populates="complaints",
    )

    category = relationship(
        "IssueCategory",
        back_populates="complaints",
    )

    location = relationship(
        "Location",
        back_populates="complaints",
    )

    media = relationship(
        "ComplaintMedia",
        back_populates="complaint",
        cascade="all, delete-orphan",
    )

    ai_analysis = relationship(
        "AIAnalysis",
        back_populates="complaint",
        uselist=False,
        cascade="all, delete-orphan",
    )

    post = relationship(
        "ComplaintPost",
        back_populates="complaint",
        uselist=False,
    )
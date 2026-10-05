from sqlalchemy import Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class AIAnalysis(Base):
    __tablename__ = "ai_analysis"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    predicted_category: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    severity: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    severity_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    confidence: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    extracted_data: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    complaint = relationship(
        "Complaint",
        back_populates="ai_analysis",
    )
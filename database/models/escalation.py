from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.base import Base


class Escalation(Base):
    __tablename__ = "escalations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id"),
        nullable=False,
        index=True,
    )

    from_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    to_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    triggered_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="active",
    )
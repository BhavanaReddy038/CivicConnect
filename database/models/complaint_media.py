import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class MediaType(str, enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"


class ComplaintMedia(Base):
    __tablename__ = "complaint_media"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id", ondelete="CASCADE"),
        nullable=False,
    )

    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    complaint = relationship(
        "Complaint",
        back_populates="media",
    )
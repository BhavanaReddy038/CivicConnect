import enum

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class PostMediaType(str, enum.Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"


class PostMedia(Base):
    __tablename__ = "post_media"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_posts.id", ondelete="CASCADE"),
        nullable=False,
    )

    media_type: Mapped[PostMediaType] = mapped_column(
        Enum(PostMediaType),
        nullable=False,
    )

    file_url: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )

    post = relationship(
        "ComplaintPost",
        back_populates="media",
    )
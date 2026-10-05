from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class ComplaintPost(Base):
    __tablename__ = "complaint_posts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey("complaints.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_visible: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )

    complaint = relationship(
        "Complaint",
        back_populates="post",
    )

    user = relationship(
        "User",
        back_populates="posts",
    )

    votes = relationship(
        "PostVote",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    comments = relationship(
        "PostComment",
        back_populates="post",
        cascade="all, delete-orphan",
    )

    media = relationship(
        "PostMedia",
        back_populates="post",
        cascade="all, delete-orphan",
    )
    
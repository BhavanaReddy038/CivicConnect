from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class PostComment(Base):
    __tablename__ = "post_comments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_posts.id", ondelete="CASCADE"),
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

    post = relationship(
        "ComplaintPost",
        back_populates="comments",
    )
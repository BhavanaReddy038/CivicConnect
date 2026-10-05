from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base


class PostVote(Base):
    __tablename__ = "post_votes"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey("complaint_posts.id", ondelete="CASCADE"),
        nullable=False,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "user_id",
            name="uq_post_user_vote",
        ),
    )

    post = relationship(
        "ComplaintPost",
        back_populates="votes",
    )
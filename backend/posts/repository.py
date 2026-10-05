from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.complaint_post import ComplaintPost
from database.models.post_comment import PostComment
from database.models.post_vote import PostVote


def create_post(
    db: Session,
    post: ComplaintPost,
):
    db.add(post)
    db.commit()
    db.refresh(post)

    return post


def get_post(
    db: Session,
    post_id: int,
):
    return db.get(
        ComplaintPost,
        post_id,
    )


def get_posts(
    db: Session,
    skip: int = 0,
    limit: int = 20,
):

    return db.scalars(
        select(ComplaintPost)
        .where(
            ComplaintPost.is_visible.is_(True)
        )
        .offset(skip)
        .limit(limit)
        .order_by(ComplaintPost.id.desc())
    ).all()


def add_vote(
    db: Session,
    vote: PostVote,
):
    db.add(vote)
    db.commit()
    db.refresh(vote)

    return vote


def find_vote(
    db: Session,
    post_id: int,
    user_id: int,
):
    return db.scalar(
        select(PostVote).where(
            PostVote.post_id == post_id,
            PostVote.user_id == user_id,
        )
    )


def add_comment(
    db: Session,
    comment: PostComment,
):
    db.add(comment)
    db.commit()
    db.refresh(comment)

    return comment


def get_comments(
    db: Session,
    post_id: int,
):

    return db.scalars(
        select(PostComment)
        .where(PostComment.post_id == post_id)
        .order_by(PostComment.id.asc())
    ).all()


def delete_comment(
    db: Session,
    comment: PostComment,
):

    db.delete(comment)
    db.commit()
    
from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.posts import repository
from backend.posts.schemas import (
    CommentCreate,
    PostCreate,
)
from database.models.complaint import Complaint
from database.models.complaint_post import ComplaintPost
from database.models.post_comment import PostComment
from database.models.post_vote import PostVote


def create_post(
    db: Session,
    user_id: int,
    data: PostCreate,
):

    complaint = db.get(
        Complaint,
        data.complaint_id,
    )

    if not complaint:
        raise HTTPException(
            status_code=404,
            detail="Complaint not found",
        )

    existing_post = complaint.post

    if existing_post:
        raise HTTPException(
            status_code=409,
            detail="A post already exists for this complaint",
        )

    post = ComplaintPost(
        complaint_id=data.complaint_id,
        user_id=user_id,
        content=data.content,
    )

    return repository.create_post(
        db,
        post,
    )


def get_post(
    db: Session,
    post_id: int,
):

    post = repository.get_post(
        db,
        post_id,
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail="Post not found",
        )

    return post


def get_posts(
    db: Session,
    skip: int,
    limit: int,
):

    return repository.get_posts(
        db,
        skip,
        limit,
    )


def vote_post(
    db: Session,
    post_id: int,
    user_id: int,
):

    post = get_post(
        db,
        post_id,
    )

    existing_vote = repository.find_vote(
        db,
        post.id,
        user_id,
    )

    if existing_vote:
        raise HTTPException(
            status_code=409,
            detail="You have already confirmed this post",
        )

    vote = PostVote(
        post_id=post.id,
        user_id=user_id,
    )

    return repository.add_vote(
        db,
        vote,
    )


def add_comment(
    db: Session,
    post_id: int,
    user_id: int,
    data: CommentCreate,
):

    get_post(
        db,
        post_id,
    )

    comment = PostComment(
        post_id=post_id,
        user_id=user_id,
        content=data.content,
    )

    return repository.add_comment(
        db,
        comment,
    )


def get_comments(
    db: Session,
    post_id: int,
):

    get_post(
        db,
        post_id,
    )

    return repository.get_comments(
        db,
        post_id,
    )


def delete_comment(
    db: Session,
    comment_id: int,
    user_id: int,
):
    comment = db.get(
        PostComment,
        comment_id,
    )

    if not comment:
        raise HTTPException(
            status_code=404,
            detail="Comment not found",
        )

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot delete this comment",
        )

    repository.delete_comment(
        db,
        comment,
    )
    
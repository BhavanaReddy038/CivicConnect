from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.auth.router import get_current_user
from backend.posts import service
from backend.posts.schemas import (
    CommentCreate,
    CommentResponse,
    PostCreate,
    PostResponse,
)
from database.database import get_db
from database.models.user import User


router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post(
    "",
    response_model=PostResponse,
    status_code=201,
)
def create_post(
    data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.create_post(
        db,
        current_user.id,
        data,
    )


@router.get(
    "",
    response_model=list[PostResponse],
)
def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):

    return service.get_posts(
        db,
        skip,
        limit,
    )


@router.get(
    "/{post_id}",
    response_model=PostResponse,
)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
):

    return service.get_post(
        db,
        post_id,
    )


@router.post(
    "/{post_id}/vote",
    status_code=201,
)
def vote_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    service.vote_post(
        db,
        post_id,
        current_user.id,
    )

    return {
        "message": "Post confirmed successfully"
    }


@router.post(
    "/{post_id}/comments",
    response_model=CommentResponse,
    status_code=201,
)
def add_comment(
    post_id: int,
    data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    return service.add_comment(
        db,
        post_id,
        current_user.id,
        data,
    )


@router.get(
    "/{post_id}/comments",
    response_model=list[CommentResponse],
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
):

    return service.get_comments(
        db,
        post_id,
    )


@router.delete(
    "/{post_id}/comments/{comment_id}",
    status_code=204,
)
def delete_comment(
        post_id: int,
        comment_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
    ):
        service.delete_comment(
            db,
            comment_id,
            current_user.id,
        )

        return None
from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    complaint_id: int
    content: str = Field(
        min_length=1,
        max_length=5000,
    )


class PostResponse(BaseModel):
    id: int
    complaint_id: int
    user_id: int
    content: str
    is_visible: bool

    model_config = {
        "from_attributes": True
    }


class CommentCreate(BaseModel):
    content: str = Field(
        min_length=1,
        max_length=2000,
    )


class CommentResponse(BaseModel):
    id: int
    post_id: int
    user_id: int
    content: str

    model_config = {
        "from_attributes": True
    }
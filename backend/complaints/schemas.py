from datetime import datetime

from pydantic import BaseModel, Field

from database.models.complaint import ComplaintStatus


class ComplaintCreate(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=200,
    )

    description: str = Field(
        min_length=10,
    )

    category_id: int | None = None

    address: str | None = None

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    affected_people: int = Field(
        default=1,
        ge=1,
    )


class ComplaintUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None
    affected_people: int | None = Field(
        default=None,
        ge=1,
    )


class ComplaintResponse(BaseModel):
    id: int
    user_id: int
    category_id: int | None
    location_id: int | None
    title: str
    description: str
    affected_people: int
    status: ComplaintStatus
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
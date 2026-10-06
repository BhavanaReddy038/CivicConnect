from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EscalationCreate(BaseModel):
    complaint_id: int
    from_level: str
    to_level: str
    reason: str


class EscalationResponse(BaseModel):
    id: int
    complaint_id: int
    from_level: str
    to_level: str
    reason: str
    triggered_at: datetime
    resolved_at: datetime | None
    status: str

    model_config = ConfigDict(from_attributes=True)
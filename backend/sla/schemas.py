from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =========================
# SLA Rule Schemas
# =========================

class SLARuleBase(BaseModel):
    department_id: int
    priority: str
    target_hours: int


class SLARuleCreate(SLARuleBase):
    pass


class SLARuleResponse(SLARuleBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# SLA Tracking Schemas
# =========================

class SLATrackingBase(BaseModel):
    complaint_id: int
    target_hours: int
    due_at: datetime


class SLATrackingCreate(SLATrackingBase):
    pass


class SLATrackingResponse(SLATrackingBase):
    id: int
    status: str
    completed_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
from datetime import datetime

from pydantic import BaseModel, ConfigDict


# =========================
# Authority Schemas
# =========================

class AuthorityBase(BaseModel):
    name: str
    code: str
    description: str | None = None


class AuthorityCreate(AuthorityBase):
    pass


class AuthorityResponse(AuthorityBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# Department Schemas
# =========================

class DepartmentBase(BaseModel):
    authority_id: int
    name: str
    code: str
    description: str | None = None


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# Officer Schemas
# =========================

class OfficerBase(BaseModel):
    department_id: int
    name: str
    email: str
    phone: str | None = None
    role: str


class OfficerCreate(OfficerBase):
    pass


class OfficerResponse(OfficerBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# =========================
# Assignment Schemas
# =========================

class AssignmentCreate(BaseModel):
    complaint_id: int
    department_id: int
    officer_id: int | None = None
    notes: str | None = None


class AssignmentResponse(BaseModel):
    id: int
    complaint_id: int
    department_id: int
    officer_id: int | None
    assigned_at: datetime
    accepted_at: datetime | None
    completed_at: datetime | None
    notes: str | None

    model_config = ConfigDict(from_attributes=True)


# =========================
# Complaint Status History
# =========================

class StatusHistoryCreate(BaseModel):
    complaint_id: int
    old_status: str | None = None
    new_status: str
    changed_by: int | None = None
    comment: str | None = None


class StatusHistoryResponse(BaseModel):
    id: int
    complaint_id: int
    old_status: str | None
    new_status: str
    changed_by: int | None
    comment: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
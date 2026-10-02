from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db

from backend.authority.schemas import (
    AssignmentCreate,
    AssignmentResponse,
    AuthorityCreate,
    AuthorityResponse,
    DepartmentCreate,
    DepartmentResponse,
    OfficerCreate,
    OfficerResponse,
    StatusHistoryCreate,
    StatusHistoryResponse,
)
from backend.authority.service import (
    AssignmentService,
    AuthorityService,
    DepartmentService,
    OfficerService,
    StatusHistoryService,
)


router = APIRouter(
    prefix="/authorities",
    tags=["Authorities"],
)


# =========================
# Authority Endpoints
# =========================

@router.post(
    "",
    response_model=AuthorityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_authority(
    data: AuthorityCreate,
    db: Session = Depends(get_db),
):
    service = AuthorityService(db)

    try:
        return service.create_authority(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "",
    response_model=list[AuthorityResponse],
)
def get_authorities(
    db: Session = Depends(get_db),
):
    service = AuthorityService(db)

    return service.get_authorities()


@router.get(
    "/{authority_id}",
    response_model=AuthorityResponse,
)
def get_authority(
    authority_id: int,
    db: Session = Depends(get_db),
):
    service = AuthorityService(db)

    authority = service.get_authority(authority_id)

    if authority is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authority not found",
        )

    return authority


@router.put(
    "/{authority_id}",
    response_model=AuthorityResponse,
)
def update_authority(
    authority_id: int,
    data: AuthorityCreate,
    db: Session = Depends(get_db),
):
    service = AuthorityService(db)

    try:
        authority = service.update_authority(
            authority_id=authority_id,
            name=data.name,
            code=data.code,
            description=data.description,
        )

        if authority is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Authority not found",
            )

        return authority

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/{authority_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_authority(
    authority_id: int,
    db: Session = Depends(get_db),
):
    service = AuthorityService(db)

    deleted = service.delete_authority(authority_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Authority not found",
        )

    return None


# =========================
# Department Endpoints
# =========================

@router.post(
    "/{authority_id}/departments",
    response_model=DepartmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_department(
    authority_id: int,
    data: DepartmentCreate,
    db: Session = Depends(get_db),
):
    service = DepartmentService(db)

    if data.authority_id != authority_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authority ID in path and request body must match",
        )

    try:
        return service.create_department(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/{authority_id}/departments",
    response_model=list[DepartmentResponse],
)
def get_departments(
    authority_id: int,
    db: Session = Depends(get_db),
):
    service = DepartmentService(db)

    return service.get_departments_by_authority(
        authority_id
    )


# =========================
# Officer Endpoints
# =========================

@router.post(
    "/departments/{department_id}/officers",
    response_model=OfficerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_officer(
    department_id: int,
    data: OfficerCreate,
    db: Session = Depends(get_db),
):
    service = OfficerService(db)

    if data.department_id != department_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department ID in path and request body must match",
        )

    try:
        return service.create_officer(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/departments/{department_id}/officers",
    response_model=list[OfficerResponse],
)
def get_officers(
    department_id: int,
    db: Session = Depends(get_db),
):
    service = OfficerService(db)

    return service.get_officers_by_department(
        department_id
    )


@router.get(
    "/departments/{department_id}/officers/active",
    response_model=list[OfficerResponse],
)
def get_active_officers(
    department_id: int,
    db: Session = Depends(get_db),
):
    service = OfficerService(db)

    return service.get_active_officers_by_department(
        department_id
    )


# =========================
# Assignment Endpoints
# =========================

@router.post(
    "/assignments",
    response_model=AssignmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assignment(
    data: AssignmentCreate,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    try:
        return service.create_assignment(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/assignments/{assignment_id}",
    response_model=AssignmentResponse,
)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    assignment = service.get_assignment(
        assignment_id
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found",
        )

    return assignment


@router.get(
    "/complaints/{complaint_id}/assignments",
    response_model=list[AssignmentResponse],
)
def get_complaint_assignments(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    return service.get_complaint_assignments(
        complaint_id
    )


@router.get(
    "/officers/{officer_id}/assignments",
    response_model=list[AssignmentResponse],
)
def get_officer_assignments(
    officer_id: int,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    return service.get_officer_assignments(
        officer_id
    )


@router.patch(
    "/assignments/{assignment_id}/accept",
    response_model=AssignmentResponse,
)
def accept_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    try:
        assignment = service.accept_assignment(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found",
            )

        return assignment

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.patch(
    "/assignments/{assignment_id}/complete",
    response_model=AssignmentResponse,
)
def complete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
):
    service = AssignmentService(db)

    try:
        assignment = service.complete_assignment(
            assignment_id
        )

        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Assignment not found",
            )

        return assignment

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


# =========================
# Complaint Status History
# =========================

@router.post(
    "/complaints/{complaint_id}/status-history",
    response_model=StatusHistoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_status_history(
    complaint_id: int,
    data: StatusHistoryCreate,
    db: Session = Depends(get_db),
):
    if data.complaint_id != complaint_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Complaint ID in path and request body must match",
        )

    service = StatusHistoryService(db)

    try:
        return service.create_history(
            complaint_id=data.complaint_id,
            old_status=data.old_status,
            new_status=data.new_status,
            changed_by=data.changed_by,
            comment=data.comment,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/complaints/{complaint_id}/status-history",
    response_model=list[StatusHistoryResponse],
)
def get_complaint_status_history(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    service = StatusHistoryService(db)

    try:
        return service.get_complaint_history(
            complaint_id
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/status-history/{history_id}",
    response_model=StatusHistoryResponse,
)
def get_status_history(
    history_id: int,
    db: Session = Depends(get_db),
):
    service = StatusHistoryService(db)

    history = service.get_history(history_id)

    if history is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Status history record not found",
        )

    return history


@router.get(
    "/complaints/{complaint_id}/status-history/latest",
    response_model=StatusHistoryResponse,
)
def get_latest_status_history(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    service = StatusHistoryService(db)

    try:
        history = service.get_latest_history(
            complaint_id
        )

        if history is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No status history found for this complaint",
            )

        return history

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
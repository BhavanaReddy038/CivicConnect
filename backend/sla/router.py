from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db

from backend.sla.escalation import (
    EscalationCreate,
    EscalationResponse,
)
from backend.sla.schemas import (
    SLARuleCreate,
    SLARuleResponse,
    SLATrackingCreate,
    SLATrackingResponse,
)
from backend.sla.service import (
    EscalationService,
    SLARuleService,
    SLATrackingService,
)


router = APIRouter(
    prefix="/sla",
    tags=["SLA"],
)


# =========================
# SLA Rule Endpoints
# =========================

@router.post(
    "/rules",
    response_model=SLARuleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sla_rule(
    data: SLARuleCreate,
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    try:
        return service.create_rule(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/rules",
    response_model=list[SLARuleResponse],
)
def get_sla_rules(
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    return service.get_rules()


@router.get(
    "/rules/{rule_id}",
    response_model=SLARuleResponse,
)
def get_sla_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    rule = service.get_rule(rule_id)

    if rule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA rule not found",
        )

    return rule


@router.get(
    "/departments/{department_id}/rules",
    response_model=list[SLARuleResponse],
)
def get_department_sla_rules(
    department_id: int,
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    return service.get_department_rules(
        department_id
    )


@router.put(
    "/rules/{rule_id}",
    response_model=SLARuleResponse,
)
def update_sla_rule(
    rule_id: int,
    data: SLARuleCreate,
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    try:
        rule = service.update_rule(
            rule_id=rule_id,
            priority=data.priority,
            target_hours=data.target_hours,
        )

        if rule is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="SLA rule not found",
            )

        return rule

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.delete(
    "/rules/{rule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_sla_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    service = SLARuleService(db)

    deleted = service.delete_rule(rule_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA rule not found",
        )

    return None


# =========================
# SLA Tracking Endpoints
# =========================

@router.post(
    "/tracking",
    response_model=SLATrackingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_sla_tracking(
    data: SLATrackingCreate,
    db: Session = Depends(get_db),
):
    service = SLATrackingService(db)

    try:
        return service.create_tracking(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/tracking/{tracking_id}",
    response_model=SLATrackingResponse,
)
def get_sla_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    service = SLATrackingService(db)

    tracking = service.get_tracking(
        tracking_id
    )

    if tracking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA tracking record not found",
        )

    return tracking


@router.get(
    "/complaints/{complaint_id}/tracking",
    response_model=SLATrackingResponse,
)
def get_complaint_sla_tracking(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    service = SLATrackingService(db)

    tracking = service.get_complaint_tracking(
        complaint_id
    )

    if tracking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA tracking record not found",
        )

    return tracking


@router.patch(
    "/tracking/{tracking_id}/complete",
    response_model=SLATrackingResponse,
)
def complete_sla_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    service = SLATrackingService(db)

    tracking = service.mark_completed(
        tracking_id
    )

    if tracking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA tracking record not found",
        )

    return tracking


@router.patch(
    "/tracking/{tracking_id}/breach",
    response_model=SLATrackingResponse,
)
def breach_sla_tracking(
    tracking_id: int,
    db: Session = Depends(get_db),
):
    service = SLATrackingService(db)

    tracking = service.mark_breached(
        tracking_id
    )

    if tracking is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA tracking record not found",
        )

    return tracking


# =========================
# Escalation Endpoints
# =========================

@router.post(
    "/escalations",
    response_model=EscalationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_escalation(
    data: EscalationCreate,
    db: Session = Depends(get_db),
):
    service = EscalationService(db)

    try:
        return service.create_escalation(
            complaint_id=data.complaint_id,
            from_level=data.from_level,
            to_level=data.to_level,
            reason=data.reason,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )


@router.get(
    "/escalations/{escalation_id}",
    response_model=EscalationResponse,
)
def get_escalation(
    escalation_id: int,
    db: Session = Depends(get_db),
):
    service = EscalationService(db)

    escalation = service.get_escalation(
        escalation_id
    )

    if escalation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escalation not found",
        )

    return escalation


@router.get(
    "/complaints/{complaint_id}/escalations",
    response_model=list[EscalationResponse],
)
def get_complaint_escalations(
    complaint_id: int,
    db: Session = Depends(get_db),
):
    service = EscalationService(db)

    return service.get_complaint_escalations(
        complaint_id
    )


@router.patch(
    "/escalations/{escalation_id}/resolve",
    response_model=EscalationResponse,
)
def resolve_escalation(
    escalation_id: int,
    db: Session = Depends(get_db),
):
    service = EscalationService(db)

    escalation = service.resolve_escalation(
        escalation_id
    )

    if escalation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escalation not found",
        )

    return escalation
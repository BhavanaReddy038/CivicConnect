from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.sla_rule import SLARule
from database.models.sla_tracking import SLATracking
from database.models.escalation import Escalation


# =========================
# SLA Rule Repository
# =========================

class SLARuleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rule: SLARule) -> SLARule:
        self.db.add(rule)
        self.db.commit()
        self.db.refresh(rule)

        return rule

    def get_by_id(self, rule_id: int) -> SLARule | None:
        statement = select(SLARule).where(
            SLARule.id == rule_id
        )

        return self.db.scalar(statement)

    def get_by_department_and_priority(
        self,
        department_id: int,
        priority: str,
    ) -> SLARule | None:
        statement = select(SLARule).where(
            SLARule.department_id == department_id,
            SLARule.priority == priority,
            SLARule.is_active.is_(True),
        )

        return self.db.scalar(statement)

    def get_by_department(
        self,
        department_id: int,
    ) -> list[SLARule]:
        statement = (
            select(SLARule)
            .where(SLARule.department_id == department_id)
            .order_by(SLARule.id)
        )

        return list(self.db.scalars(statement).all())

    def get_all(self) -> list[SLARule]:
        statement = select(SLARule).order_by(SLARule.id)

        return list(self.db.scalars(statement).all())

    def update(
        self,
        rule: SLARule,
        priority: str | None = None,
        target_hours: int | None = None,
        is_active: bool | None = None,
    ) -> SLARule:
        if priority is not None:
            rule.priority = priority

        if target_hours is not None:
            rule.target_hours = target_hours

        if is_active is not None:
            rule.is_active = is_active

        self.db.commit()
        self.db.refresh(rule)

        return rule

    def delete(self, rule: SLARule) -> None:
        self.db.delete(rule)
        self.db.commit()


# =========================
# SLA Tracking Repository
# =========================

class SLATrackingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, tracking: SLATracking) -> SLATracking:
        self.db.add(tracking)
        self.db.commit()
        self.db.refresh(tracking)

        return tracking

    def get_by_id(
        self,
        tracking_id: int,
    ) -> SLATracking | None:
        statement = select(SLATracking).where(
            SLATracking.id == tracking_id
        )

        return self.db.scalar(statement)

    def get_by_complaint(
        self,
        complaint_id: int,
    ) -> SLATracking | None:
        statement = (
            select(SLATracking)
            .where(SLATracking.complaint_id == complaint_id)
            .order_by(SLATracking.created_at.desc())
        )

        return self.db.scalars(statement).first()

    def get_active(
        self,
        complaint_id: int,
    ) -> SLATracking | None:
        statement = select(SLATracking).where(
            SLATracking.complaint_id == complaint_id,
            SLATracking.status == "active",
        )

        return self.db.scalar(statement)

    def update_status(
        self,
        tracking: SLATracking,
        status: str,
        completed_at=None,
    ) -> SLATracking:
        tracking.status = status

        if completed_at is not None:
            tracking.completed_at = completed_at

        self.db.commit()
        self.db.refresh(tracking)

        return tracking


# =========================
# Escalation Repository
# =========================

class EscalationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        escalation: Escalation,
    ) -> Escalation:
        self.db.add(escalation)
        self.db.commit()
        self.db.refresh(escalation)

        return escalation

    def get_by_id(
        self,
        escalation_id: int,
    ) -> Escalation | None:
        statement = select(Escalation).where(
            Escalation.id == escalation_id
        )

        return self.db.scalar(statement)

    def get_by_complaint(
        self,
        complaint_id: int,
    ) -> list[Escalation]:
        statement = (
            select(Escalation)
            .where(Escalation.complaint_id == complaint_id)
            .order_by(Escalation.triggered_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def get_active_by_complaint(
        self,
        complaint_id: int,
    ) -> Escalation | None:
        statement = select(Escalation).where(
            Escalation.complaint_id == complaint_id,
            Escalation.status == "active",
        )

        return self.db.scalar(statement)

    def resolve(
        self,
        escalation: Escalation,
        resolved_at,
    ) -> Escalation:
        escalation.status = "resolved"
        escalation.resolved_at = resolved_at

        self.db.commit()
        self.db.refresh(escalation)

        return escalation
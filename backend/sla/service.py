from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.models.escalation import Escalation
from database.models.sla_rule import SLARule
from database.models.sla_tracking import SLATracking

from backend.sla.repository import (
    EscalationRepository,
    SLARuleRepository,
    SLATrackingRepository,
)
from backend.sla.schemas import (
    SLARuleCreate,
    SLATrackingCreate,
)


# =========================
# SLA Rule Service
# =========================

class SLARuleService:
    def __init__(self, db: Session):
        self.repository = SLARuleRepository(db)

    def create_rule(
        self,
        data: SLARuleCreate,
    ) -> SLARule:
        existing_rule = (
            self.repository.get_by_department_and_priority(
                data.department_id,
                data.priority,
            )
        )

        if existing_rule:
            raise ValueError(
                "An active SLA rule already exists for "
                f"department {data.department_id} "
                f"and priority '{data.priority}'"
            )

        if data.target_hours <= 0:
            raise ValueError(
                "target_hours must be greater than 0"
            )

        rule = SLARule(
            department_id=data.department_id,
            priority=data.priority,
            target_hours=data.target_hours,
        )

        return self.repository.create(rule)

    def get_rule(
        self,
        rule_id: int,
    ) -> SLARule | None:
        return self.repository.get_by_id(rule_id)

    def get_rules(self) -> list[SLARule]:
        return self.repository.get_all()

    def get_department_rules(
        self,
        department_id: int,
    ) -> list[SLARule]:
        return self.repository.get_by_department(
            department_id
        )

    def update_rule(
        self,
        rule_id: int,
        priority: str | None = None,
        target_hours: int | None = None,
        is_active: bool | None = None,
    ) -> SLARule | None:
        rule = self.repository.get_by_id(rule_id)

        if rule is None:
            return None

        if target_hours is not None and target_hours <= 0:
            raise ValueError(
                "target_hours must be greater than 0"
            )

        if (
            priority is not None
            and priority != rule.priority
        ):
            existing_rule = (
                self.repository.get_by_department_and_priority(
                    rule.department_id,
                    priority,
                )
            )

            if existing_rule and existing_rule.id != rule.id:
                raise ValueError(
                    "An active SLA rule already exists for "
                    f"department {rule.department_id} "
                    f"and priority '{priority}'"
                )

        return self.repository.update(
            rule=rule,
            priority=priority,
            target_hours=target_hours,
            is_active=is_active,
        )

    def delete_rule(
        self,
        rule_id: int,
    ) -> bool:
        rule = self.repository.get_by_id(rule_id)

        if rule is None:
            return False

        self.repository.delete(rule)

        return True


# =========================
# SLA Tracking Service
# =========================

class SLATrackingService:
    def __init__(self, db: Session):
        self.repository = SLATrackingRepository(db)

    def create_tracking(
        self,
        data: SLATrackingCreate,
    ) -> SLATracking:
        if data.target_hours <= 0:
            raise ValueError(
                "target_hours must be greater than 0"
            )

        existing_tracking = self.repository.get_active(
            data.complaint_id
        )

        if existing_tracking:
            raise ValueError(
                f"An active SLA already exists for "
                f"complaint {data.complaint_id}"
            )

        tracking = SLATracking(
            complaint_id=data.complaint_id,
            target_hours=data.target_hours,
            due_at=data.due_at,
            status="active",
        )

        return self.repository.create(tracking)

    def create_tracking_from_rule(
        self,
        complaint_id: int,
        target_hours: int,
    ) -> SLATracking:
        if target_hours <= 0:
            raise ValueError(
                "target_hours must be greater than 0"
            )

        existing_tracking = self.repository.get_active(
            complaint_id
        )

        if existing_tracking:
            raise ValueError(
                f"An active SLA already exists for "
                f"complaint {complaint_id}"
            )

        created_at = datetime.utcnow()

        due_at = created_at + timedelta(
            hours=target_hours
        )

        tracking = SLATracking(
            complaint_id=complaint_id,
            target_hours=target_hours,
            due_at=due_at,
            status="active",
            created_at=created_at,
        )

        return self.repository.create(tracking)

    def get_tracking(
        self,
        tracking_id: int,
    ) -> SLATracking | None:
        return self.repository.get_by_id(tracking_id)

    def get_complaint_tracking(
        self,
        complaint_id: int,
    ) -> SLATracking | None:
        return self.repository.get_by_complaint(
            complaint_id
        )

    def mark_completed(
        self,
        tracking_id: int,
    ) -> SLATracking | None:
        tracking = self.repository.get_by_id(tracking_id)

        if tracking is None:
            return None

        completed_at = datetime.utcnow()

        if completed_at <= tracking.due_at:
            status = "met"
        else:
            status = "breached"

        return self.repository.update_status(
            tracking=tracking,
            status=status,
            completed_at=completed_at,
        )

    def mark_breached(
        self,
        tracking_id: int,
    ) -> SLATracking | None:
        tracking = self.repository.get_by_id(tracking_id)

        if tracking is None:
            return None

        return self.repository.update_status(
            tracking=tracking,
            status="breached",
        )


# =========================
# Escalation Service
# =========================

class EscalationService:
    def __init__(self, db: Session):
        self.repository = EscalationRepository(db)

    def create_escalation(
        self,
        complaint_id: int,
        from_level: str,
        to_level: str,
        reason: str,
    ) -> Escalation:
        if from_level == to_level:
            raise ValueError(
                "from_level and to_level must be different"
            )

        active_escalation = (
            self.repository.get_active_by_complaint(
                complaint_id
            )
        )

        if active_escalation:
            raise ValueError(
                f"Complaint {complaint_id} already has "
                "an active escalation"
            )

        escalation = Escalation(
            complaint_id=complaint_id,
            from_level=from_level,
            to_level=to_level,
            reason=reason,
            status="active",
        )

        return self.repository.create(escalation)

    def get_escalation(
        self,
        escalation_id: int,
    ) -> Escalation | None:
        return self.repository.get_by_id(escalation_id)

    def get_complaint_escalations(
        self,
        complaint_id: int,
    ) -> list[Escalation]:
        return self.repository.get_by_complaint(
            complaint_id
        )

    def resolve_escalation(
        self,
        escalation_id: int,
    ) -> Escalation | None:
        escalation = self.repository.get_by_id(
            escalation_id
        )

        if escalation is None:
            return None

        if escalation.status == "resolved":
            return escalation

        return self.repository.resolve(
            escalation=escalation,
            resolved_at=datetime.utcnow(),
        )
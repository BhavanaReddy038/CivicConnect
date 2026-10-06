from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from backend.sla.schemas import (
    SLARuleCreate,
    SLATrackingCreate,
)
from backend.sla.service import (
    EscalationService,
    SLARuleService,
    SLATrackingService,
)


# ============================================================
# Helper Functions
# ============================================================


def create_sla_rule_service():
    db = MagicMock()
    service = SLARuleService(db)

    service.repository.get_by_department_and_priority = MagicMock()
    service.repository.create = MagicMock()
    service.repository.get_by_id = MagicMock()
    service.repository.get_all = MagicMock()
    service.repository.get_by_department = MagicMock()
    service.repository.update = MagicMock()
    service.repository.delete = MagicMock()

    return service


def create_sla_tracking_service():
    db = MagicMock()
    service = SLATrackingService(db)

    service.repository.get_active = MagicMock()
    service.repository.create = MagicMock()
    service.repository.get_by_id = MagicMock()
    service.repository.get_by_complaint = MagicMock()
    service.repository.update_status = MagicMock()

    return service


def create_escalation_service():
    db = MagicMock()
    service = EscalationService(db)

    service.repository.get_active_by_complaint = MagicMock()
    service.repository.create = MagicMock()
    service.repository.get_by_id = MagicMock()
    service.repository.get_by_complaint = MagicMock()
    service.repository.resolve = MagicMock()

    return service


# ============================================================
# SLA RULE TESTS
# ============================================================


def test_create_sla_rule():
    service = create_sla_rule_service()

    expected_rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
        target_hours=24,
        is_active=True,
    )

    service.repository.get_by_department_and_priority = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=expected_rule
    )

    data = SLARuleCreate(
        department_id=1,
        priority="high",
        target_hours=24,
    )

    result = service.create_rule(data)

    assert result.id == 1
    assert result.department_id == 1
    assert result.priority == "high"
    assert result.target_hours == 24
    assert result.is_active is True

    service.repository.get_by_department_and_priority.assert_called_once_with(
        1,
        "high",
    )
    service.repository.create.assert_called_once()


def test_create_sla_rule_rejects_duplicate():
    service = create_sla_rule_service()

    existing_rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
    )

    service.repository.get_by_department_and_priority = MagicMock(
        return_value=existing_rule
    )

    data = SLARuleCreate(
        department_id=1,
        priority="high",
        target_hours=24,
    )

    with pytest.raises(
        ValueError,
        match="An active SLA rule already exists",
    ):
        service.create_rule(data)

    service.repository.create.assert_not_called()


def test_create_sla_rule_rejects_invalid_target_hours():
    service = create_sla_rule_service()

    service.repository.get_by_department_and_priority = MagicMock(
        return_value=None
    )

    data = SLARuleCreate(
        department_id=1,
        priority="high",
        target_hours=0,
    )

    with pytest.raises(
        ValueError,
        match="target_hours must be greater than 0",
    ):
        service.create_rule(data)

    service.repository.create.assert_not_called()


def test_get_sla_rule():
    service = create_sla_rule_service()

    rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
        target_hours=24,
    )

    service.repository.get_by_id = MagicMock(
        return_value=rule
    )

    result = service.get_rule(1)

    assert result.id == 1
    assert result.priority == "high"
    assert result.target_hours == 24

    service.repository.get_by_id.assert_called_once_with(1)


def test_get_sla_rule_returns_none_when_not_found():
    service = create_sla_rule_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_rule(999)

    assert result is None


def test_get_sla_rules():
    service = create_sla_rule_service()

    rules = [
        MagicMock(
            id=1,
            department_id=1,
            priority="high",
            target_hours=24,
        ),
        MagicMock(
            id=2,
            department_id=1,
            priority="medium",
            target_hours=48,
        ),
    ]

    service.repository.get_all = MagicMock(
        return_value=rules
    )

    result = service.get_rules()

    assert len(result) == 2
    assert result[0].priority == "high"
    assert result[1].priority == "medium"

    service.repository.get_all.assert_called_once()


def test_get_department_rules():
    service = create_sla_rule_service()

    rules = [
        MagicMock(
            id=1,
            department_id=1,
            priority="high",
        ),
        MagicMock(
            id=2,
            department_id=1,
            priority="medium",
        ),
    ]

    service.repository.get_by_department = MagicMock(
        return_value=rules
    )

    result = service.get_department_rules(1)

    assert len(result) == 2
    assert result[0].department_id == 1
    assert result[1].department_id == 1

    service.repository.get_by_department.assert_called_once_with(1)


def test_update_sla_rule():
    service = create_sla_rule_service()

    rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
        target_hours=24,
        is_active=True,
    )

    updated_rule = MagicMock(
        id=1,
        department_id=1,
        priority="critical",
        target_hours=12,
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=rule
    )

    service.repository.get_by_department_and_priority = MagicMock(
        return_value=None
    )

    service.repository.update = MagicMock(
        return_value=updated_rule
    )

    result = service.update_rule(
        rule_id=1,
        priority="critical",
        target_hours=12,
        is_active=True,
    )

    assert result.id == 1
    assert result.priority == "critical"
    assert result.target_hours == 12

    service.repository.update.assert_called_once()


def test_update_sla_rule_returns_none_when_not_found():
    service = create_sla_rule_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.update_rule(
        rule_id=999,
        target_hours=24,
    )

    assert result is None


def test_update_sla_rule_rejects_invalid_target_hours():
    service = create_sla_rule_service()

    rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
    )

    service.repository.get_by_id = MagicMock(
        return_value=rule
    )

    with pytest.raises(
        ValueError,
        match="target_hours must be greater than 0",
    ):
        service.update_rule(
            rule_id=1,
            target_hours=0,
        )

    service.repository.update.assert_not_called()


def test_update_sla_rule_rejects_duplicate_priority():
    service = create_sla_rule_service()

    rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
    )

    existing_rule = MagicMock(
        id=2,
        department_id=1,
        priority="critical",
    )

    service.repository.get_by_id = MagicMock(
        return_value=rule
    )

    service.repository.get_by_department_and_priority = MagicMock(
        return_value=existing_rule
    )

    with pytest.raises(
        ValueError,
        match="An active SLA rule already exists",
    ):
        service.update_rule(
            rule_id=1,
            priority="critical",
        )

    service.repository.update.assert_not_called()


def test_delete_sla_rule():
    service = create_sla_rule_service()

    rule = MagicMock(
        id=1,
        department_id=1,
        priority="high",
    )

    service.repository.get_by_id = MagicMock(
        return_value=rule
    )

    result = service.delete_rule(1)

    assert result is True

    service.repository.delete.assert_called_once_with(rule)


def test_delete_sla_rule_returns_false_when_not_found():
    service = create_sla_rule_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.delete_rule(999)

    assert result is False

    service.repository.delete.assert_not_called()


# ============================================================
# SLA TRACKING TESTS
# ============================================================


def test_create_sla_tracking():
    service = create_sla_tracking_service()

    due_at = datetime.utcnow() + timedelta(hours=24)

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        target_hours=24,
        due_at=due_at,
        status="active",
    )

    service.repository.get_active = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=tracking
    )

    data = SLATrackingCreate(
        complaint_id=101,
        target_hours=24,
        due_at=due_at,
    )

    result = service.create_tracking(data)

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.target_hours == 24
    assert result.status == "active"

    service.repository.get_active.assert_called_once_with(101)
    service.repository.create.assert_called_once()


def test_create_sla_tracking_rejects_invalid_target_hours():
    service = create_sla_tracking_service()

    due_at = datetime.utcnow() + timedelta(hours=24)

    data = SLATrackingCreate(
        complaint_id=101,
        target_hours=0,
        due_at=due_at,
    )

    with pytest.raises(
        ValueError,
        match="target_hours must be greater than 0",
    ):
        service.create_tracking(data)

    service.repository.create.assert_not_called()


def test_create_sla_tracking_rejects_existing_active_tracking():
    service = create_sla_tracking_service()

    existing_tracking = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    service.repository.get_active = MagicMock(
        return_value=existing_tracking
    )

    due_at = datetime.utcnow() + timedelta(hours=24)

    data = SLATrackingCreate(
        complaint_id=101,
        target_hours=24,
        due_at=due_at,
    )

    with pytest.raises(
        ValueError,
        match="An active SLA already exists for complaint 101",
    ):
        service.create_tracking(data)

    service.repository.create.assert_not_called()


def test_create_tracking_from_rule():
    service = create_sla_tracking_service()

    expected_tracking = MagicMock(
        id=1,
        complaint_id=101,
        target_hours=24,
        status="active",
    )

    service.repository.get_active = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=expected_tracking
    )

    result = service.create_tracking_from_rule(
        complaint_id=101,
        target_hours=24,
    )

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.target_hours == 24
    assert result.status == "active"

    tracking = service.repository.create.call_args[0][0]

    assert tracking.complaint_id == 101
    assert tracking.target_hours == 24
    assert tracking.status == "active"
    assert tracking.due_at > tracking.created_at


def test_create_tracking_from_rule_rejects_invalid_target_hours():
    service = create_sla_tracking_service()

    with pytest.raises(
        ValueError,
        match="target_hours must be greater than 0",
    ):
        service.create_tracking_from_rule(
            complaint_id=101,
            target_hours=0,
        )

    service.repository.create.assert_not_called()


def test_create_tracking_from_rule_rejects_existing_active_tracking():
    service = create_sla_tracking_service()

    service.repository.get_active = MagicMock(
        return_value=MagicMock(
            id=1,
            complaint_id=101,
        )
    )

    with pytest.raises(
        ValueError,
        match="An active SLA already exists for complaint 101",
    ):
        service.create_tracking_from_rule(
            complaint_id=101,
            target_hours=24,
        )

    service.repository.create.assert_not_called()


def test_get_sla_tracking():
    service = create_sla_tracking_service()

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    service.repository.get_by_id = MagicMock(
        return_value=tracking
    )

    result = service.get_tracking(1)

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.status == "active"


def test_get_sla_tracking_returns_none_when_not_found():
    service = create_sla_tracking_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_tracking(999)

    assert result is None


def test_get_complaint_tracking():
    service = create_sla_tracking_service()

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    service.repository.get_by_complaint = MagicMock(
        return_value=tracking
    )

    result = service.get_complaint_tracking(101)

    assert result.id == 1
    assert result.complaint_id == 101

    service.repository.get_by_complaint.assert_called_once_with(101)


def test_mark_completed_before_due_date():
    service = create_sla_tracking_service()

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        due_at=datetime.utcnow() + timedelta(hours=24),
        status="active",
    )

    updated_tracking = MagicMock(
        id=1,
        status="met",
    )

    service.repository.get_by_id = MagicMock(
        return_value=tracking
    )

    service.repository.update_status = MagicMock(
        return_value=updated_tracking
    )

    result = service.mark_completed(1)

    assert result.id == 1
    assert result.status == "met"

    service.repository.update_status.assert_called_once()

    call_kwargs = service.repository.update_status.call_args.kwargs

    assert call_kwargs["tracking"] is tracking
    assert call_kwargs["status"] == "met"
    assert call_kwargs["completed_at"] is not None


def test_mark_completed_after_due_date():
    service = create_sla_tracking_service()

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        due_at=datetime.utcnow() - timedelta(hours=1),
        status="active",
    )

    updated_tracking = MagicMock(
        id=1,
        status="breached",
    )

    service.repository.get_by_id = MagicMock(
        return_value=tracking
    )

    service.repository.update_status = MagicMock(
        return_value=updated_tracking
    )

    result = service.mark_completed(1)

    assert result.id == 1
    assert result.status == "breached"

    call_kwargs = service.repository.update_status.call_args.kwargs

    assert call_kwargs["tracking"] is tracking
    assert call_kwargs["status"] == "breached"
    assert call_kwargs["completed_at"] is not None


def test_mark_completed_returns_none_when_not_found():
    service = create_sla_tracking_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.mark_completed(999)

    assert result is None

    service.repository.update_status.assert_not_called()


def test_mark_breached():
    service = create_sla_tracking_service()

    tracking = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    breached_tracking = MagicMock(
        id=1,
        complaint_id=101,
        status="breached",
    )

    service.repository.get_by_id = MagicMock(
        return_value=tracking
    )

    service.repository.update_status = MagicMock(
        return_value=breached_tracking
    )

    result = service.mark_breached(1)

    assert result.id == 1
    assert result.status == "breached"

    service.repository.update_status.assert_called_once_with(
        tracking=tracking,
        status="breached",
    )


def test_mark_breached_returns_none_when_not_found():
    service = create_sla_tracking_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.mark_breached(999)

    assert result is None

    service.repository.update_status.assert_not_called()


# ============================================================
# ESCALATION TESTS
# ============================================================


def test_create_escalation():
    service = create_escalation_service()

    escalation = MagicMock(
        id=1,
        complaint_id=101,
        from_level="department",
        to_level="authority",
        reason="SLA breached",
        status="active",
    )

    service.repository.get_active_by_complaint = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=escalation
    )

    result = service.create_escalation(
        complaint_id=101,
        from_level="department",
        to_level="authority",
        reason="SLA breached",
    )

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.from_level == "department"
    assert result.to_level == "authority"
    assert result.reason == "SLA breached"
    assert result.status == "active"

    service.repository.get_active_by_complaint.assert_called_once_with(
        101
    )
    service.repository.create.assert_called_once()


def test_create_escalation_rejects_same_level():
    service = create_escalation_service()

    with pytest.raises(
        ValueError,
        match="from_level and to_level must be different",
    ):
        service.create_escalation(
            complaint_id=101,
            from_level="department",
            to_level="department",
            reason="SLA breached",
        )

    service.repository.create.assert_not_called()


def test_create_escalation_rejects_existing_active_escalation():
    service = create_escalation_service()

    service.repository.get_active_by_complaint = MagicMock(
        return_value=MagicMock(
            id=1,
            complaint_id=101,
            status="active",
        )
    )

    with pytest.raises(
        ValueError,
        match="Complaint 101 already has an active escalation",
    ):
        service.create_escalation(
            complaint_id=101,
            from_level="department",
            to_level="authority",
            reason="SLA breached",
        )

    service.repository.create.assert_not_called()


def test_get_escalation():
    service = create_escalation_service()

    escalation = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    service.repository.get_by_id = MagicMock(
        return_value=escalation
    )

    result = service.get_escalation(1)

    assert result.id == 1
    assert result.complaint_id == 101


def test_get_escalation_returns_none_when_not_found():
    service = create_escalation_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_escalation(999)

    assert result is None


def test_get_complaint_escalations():
    service = create_escalation_service()

    escalations = [
        MagicMock(
            id=1,
            complaint_id=101,
            from_level="department",
            to_level="authority",
        ),
        MagicMock(
            id=2,
            complaint_id=101,
            from_level="authority",
            to_level="admin",
        ),
    ]

    service.repository.get_by_complaint = MagicMock(
        return_value=escalations
    )

    result = service.get_complaint_escalations(101)

    assert len(result) == 2
    assert result[0].complaint_id == 101
    assert result[1].complaint_id == 101

    service.repository.get_by_complaint.assert_called_once_with(
        101
    )


def test_resolve_escalation():
    service = create_escalation_service()

    escalation = MagicMock(
        id=1,
        complaint_id=101,
        status="active",
    )

    resolved_escalation = MagicMock(
        id=1,
        complaint_id=101,
        status="resolved",
    )

    service.repository.get_by_id = MagicMock(
        return_value=escalation
    )

    service.repository.resolve = MagicMock(
        return_value=resolved_escalation
    )

    result = service.resolve_escalation(1)

    assert result.id == 1
    assert result.status == "resolved"

    service.repository.resolve.assert_called_once()

    call_kwargs = service.repository.resolve.call_args.kwargs

    assert call_kwargs["escalation"] is escalation
    assert call_kwargs["resolved_at"] is not None


def test_resolve_escalation_returns_none_when_not_found():
    service = create_escalation_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.resolve_escalation(999)

    assert result is None

    service.repository.resolve.assert_not_called()


def test_resolve_escalation_returns_existing_resolved():
    service = create_escalation_service()

    escalation = MagicMock(
        id=1,
        complaint_id=101,
        status="resolved",
    )

    service.repository.get_by_id = MagicMock(
        return_value=escalation
    )

    result = service.resolve_escalation(1)

    assert result is escalation

    service.repository.resolve.assert_not_called()
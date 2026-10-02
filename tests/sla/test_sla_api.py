from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


# ============================================================
# SLA RULE API TESTS
# ============================================================


def test_create_sla_rule():
    rule = MagicMock()
    rule.id = 1
    rule.department_id = 1
    rule.priority = "high"
    rule.target_hours = 24
    rule.is_active = True

    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.create_rule.return_value = rule

        response = client.post(
            "/api/sla/rules",
            json={
                "department_id": 1,
                "priority": "high",
                "target_hours": 24,
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["department_id"] == 1
    assert data["priority"] == "high"
    assert data["target_hours"] == 24
    assert data["is_active"] is True


def test_create_sla_rule_validation_error():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.create_rule.side_effect = ValueError(
            "An active SLA rule already exists for department 1 and priority 'high'"
        )

        response = client.post(
            "/api/sla/rules",
            json={
                "department_id": 1,
                "priority": "high",
                "target_hours": 24,
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An active SLA rule already exists for department 1 and priority 'high'"
    )


def test_get_sla_rules():
    rule = MagicMock()
    rule.id = 1
    rule.department_id = 1
    rule.priority = "high"
    rule.target_hours = 24
    rule.is_active = True

    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.get_rules.return_value = [rule]

        response = client.get("/api/sla/rules")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["priority"] == "high"


def test_get_sla_rule():
    rule = MagicMock()
    rule.id = 1
    rule.department_id = 1
    rule.priority = "high"
    rule.target_hours = 24
    rule.is_active = True

    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.get_rule.return_value = rule

        response = client.get("/api/sla/rules/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["department_id"] == 1
    assert data["priority"] == "high"


def test_get_sla_rule_not_found():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.get_rule.return_value = None

        response = client.get("/api/sla/rules/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "SLA rule not found"


def test_get_department_sla_rules():
    rule = MagicMock()
    rule.id = 1
    rule.department_id = 5
    rule.priority = "critical"
    rule.target_hours = 4
    rule.is_active = True

    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.get_department_rules.return_value = [rule]

        response = client.get(
            "/api/sla/departments/5/rules"
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["department_id"] == 5
    assert data[0]["priority"] == "critical"


def test_update_sla_rule():
    rule = MagicMock()
    rule.id = 1
    rule.department_id = 1
    rule.priority = "critical"
    rule.target_hours = 12
    rule.is_active = True

    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.update_rule.return_value = rule

        response = client.put(
            "/api/sla/rules/1",
            json={
                "department_id": 1,
                "priority": "critical",
                "target_hours": 12,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["priority"] == "critical"
    assert data["target_hours"] == 12


def test_update_sla_rule_not_found():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.update_rule.return_value = None

        response = client.put(
            "/api/sla/rules/999",
            json={
                "department_id": 1,
                "priority": "high",
                "target_hours": 24,
            },
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "SLA rule not found"


def test_update_sla_rule_validation_error():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.update_rule.side_effect = ValueError(
            "target_hours must be greater than 0"
        )

        response = client.put(
            "/api/sla/rules/1",
            json={
                "department_id": 1,
                "priority": "high",
                "target_hours": 0,
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "target_hours must be greater than 0"
    )


def test_delete_sla_rule():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.delete_rule.return_value = True

        response = client.delete("/api/sla/rules/1")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_sla_rule_not_found():
    with patch(
        "backend.sla.router.SLARuleService"
    ) as service_class:
        service = service_class.return_value
        service.delete_rule.return_value = False

        response = client.delete("/api/sla/rules/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "SLA rule not found"


# ============================================================
# SLA TRACKING API TESTS
# ============================================================


def test_create_sla_tracking():
    due_at = datetime.utcnow() + timedelta(hours=24)

    tracking = MagicMock()
    tracking.id = 1
    tracking.complaint_id = 101
    tracking.target_hours = 24
    tracking.due_at = due_at
    tracking.status = "active"
    tracking.completed_at = None
    tracking.created_at = datetime.utcnow()

    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.create_tracking.return_value = tracking

        response = client.post(
            "/api/sla/tracking",
            json={
                "complaint_id": 101,
                "target_hours": 24,
                "due_at": due_at.isoformat(),
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["target_hours"] == 24
    assert data["status"] == "active"


def test_create_sla_tracking_validation_error():
    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.create_tracking.side_effect = ValueError(
            "An active SLA already exists for complaint 101"
        )

        response = client.post(
            "/api/sla/tracking",
            json={
                "complaint_id": 101,
                "target_hours": 24,
                "due_at": (
                    datetime.utcnow() + timedelta(hours=24)
                ).isoformat(),
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "An active SLA already exists for complaint 101"
    )


def test_get_sla_tracking():
    tracking = MagicMock()
    tracking.id = 1
    tracking.complaint_id = 101
    tracking.target_hours = 24
    tracking.due_at = datetime.utcnow() + timedelta(hours=24)
    tracking.status = "active"
    tracking.completed_at = None
    tracking.created_at = datetime.utcnow()

    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.get_tracking.return_value = tracking

        response = client.get("/api/sla/tracking/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["status"] == "active"


def test_get_sla_tracking_not_found():
    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.get_tracking.return_value = None

        response = client.get("/api/sla/tracking/999")

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "SLA tracking record not found"
    )


def test_get_complaint_sla_tracking():
    tracking = MagicMock()
    tracking.id = 1
    tracking.complaint_id = 101
    tracking.target_hours = 24
    tracking.due_at = datetime.utcnow() + timedelta(hours=24)
    tracking.status = "active"
    tracking.completed_at = None
    tracking.created_at = datetime.utcnow()

    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.get_complaint_tracking.return_value = tracking

        response = client.get(
            "/api/sla/complaints/101/tracking"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["complaint_id"] == 101
    assert data["status"] == "active"


def test_get_complaint_sla_tracking_not_found():
    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.get_complaint_tracking.return_value = None

        response = client.get(
            "/api/sla/complaints/999/tracking"
        )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "SLA tracking record not found"
    )


def test_complete_sla_tracking():
    tracking = MagicMock()
    tracking.id = 1
    tracking.complaint_id = 101
    tracking.target_hours = 24
    tracking.due_at = datetime.utcnow() + timedelta(hours=24)
    tracking.status = "met"
    tracking.completed_at = datetime.utcnow()
    tracking.created_at = datetime.utcnow()

    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.mark_completed.return_value = tracking

        response = client.patch(
            "/api/sla/tracking/1/complete"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "met"


def test_complete_sla_tracking_not_found():
    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.mark_completed.return_value = None

        response = client.patch(
            "/api/sla/tracking/999/complete"
        )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "SLA tracking record not found"
    )


def test_breach_sla_tracking():
    tracking = MagicMock()
    tracking.id = 1
    tracking.complaint_id = 101
    tracking.target_hours = 24
    tracking.due_at = datetime.utcnow() - timedelta(hours=1)
    tracking.status = "breached"
    tracking.completed_at = None
    tracking.created_at = datetime.utcnow()

    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.mark_breached.return_value = tracking

        response = client.patch(
            "/api/sla/tracking/1/breach"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "breached"


def test_breach_sla_tracking_not_found():
    with patch(
        "backend.sla.router.SLATrackingService"
    ) as service_class:
        service = service_class.return_value
        service.mark_breached.return_value = None

        response = client.patch(
            "/api/sla/tracking/999/breach"
        )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "SLA tracking record not found"
    )


# ============================================================
# ESCALATION API TESTS
# ============================================================


def test_create_escalation():
    escalation = MagicMock()
    escalation.id = 1
    escalation.complaint_id = 101
    escalation.from_level = "department"
    escalation.to_level = "authority"
    escalation.reason = "SLA breached"
    escalation.triggered_at = datetime.utcnow()
    escalation.resolved_at = None
    escalation.status = "active"

    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.create_escalation.return_value = escalation

        response = client.post(
            "/api/sla/escalations",
            json={
                "complaint_id": 101,
                "from_level": "department",
                "to_level": "authority",
                "reason": "SLA breached",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["from_level"] == "department"
    assert data["to_level"] == "authority"
    assert data["status"] == "active"


def test_create_escalation_validation_error():
    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.create_escalation.side_effect = ValueError(
            "from_level and to_level must be different"
        )

        response = client.post(
            "/api/sla/escalations",
            json={
                "complaint_id": 101,
                "from_level": "department",
                "to_level": "department",
                "reason": "SLA breached",
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "from_level and to_level must be different"
    )


def test_create_escalation_existing_active():
    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.create_escalation.side_effect = ValueError(
            "Complaint 101 already has an active escalation"
        )

        response = client.post(
            "/api/sla/escalations",
            json={
                "complaint_id": 101,
                "from_level": "department",
                "to_level": "authority",
                "reason": "SLA breached",
            },
        )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Complaint 101 already has an active escalation"
    )


def test_get_escalation():
    escalation = MagicMock()
    escalation.id = 1
    escalation.complaint_id = 101
    escalation.from_level = "department"
    escalation.to_level = "authority"
    escalation.reason = "SLA breached"
    escalation.triggered_at = datetime.utcnow()
    escalation.resolved_at = None
    escalation.status = "active"

    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.get_escalation.return_value = escalation

        response = client.get("/api/sla/escalations/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["status"] == "active"


def test_get_escalation_not_found():
    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.get_escalation.return_value = None

        response = client.get(
            "/api/sla/escalations/999"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Escalation not found"


def test_get_complaint_escalations():
    escalation = MagicMock()
    escalation.id = 1
    escalation.complaint_id = 101
    escalation.from_level = "department"
    escalation.to_level = "authority"
    escalation.reason = "SLA breached"
    escalation.triggered_at = datetime.utcnow()
    escalation.resolved_at = None
    escalation.status = "active"

    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.get_complaint_escalations.return_value = [
            escalation
        ]

        response = client.get(
            "/api/sla/complaints/101/escalations"
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["complaint_id"] == 101
    assert data[0]["status"] == "active"


def test_resolve_escalation():
    escalation = MagicMock()
    escalation.id = 1
    escalation.complaint_id = 101
    escalation.from_level = "department"
    escalation.to_level = "authority"
    escalation.reason = "SLA breached"
    escalation.triggered_at = datetime.utcnow()
    escalation.resolved_at = datetime.utcnow()
    escalation.status = "resolved"

    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.resolve_escalation.return_value = escalation

        response = client.patch(
            "/api/sla/escalations/1/resolve"
        )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["status"] == "resolved"


def test_resolve_escalation_not_found():
    with patch(
        "backend.sla.router.EscalationService"
    ) as service_class:
        service = service_class.return_value
        service.resolve_escalation.return_value = None

        response = client.patch(
            "/api/sla/escalations/999/resolve"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Escalation not found"
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


# ============================================================
# Authority API Tests
# ============================================================


def test_create_authority():
    mock_authority = MagicMock()
    mock_authority.id = 1
    mock_authority.name = "Greater Hyderabad Municipal Corporation"
    mock_authority.code = "GHMC"
    mock_authority.description = "Hyderabad municipal authority"
    mock_authority.is_active = True

    with patch(
        "backend.authority.router.AuthorityService"
    ) as service_class:
        service = service_class.return_value
        service.create_authority.return_value = mock_authority

        response = client.post(
            "/api/authorities",
            json={
                "name": "Greater Hyderabad Municipal Corporation",
                "code": "GHMC",
                "description": "Hyderabad municipal authority",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Greater Hyderabad Municipal Corporation"
    assert data["code"] == "GHMC"
    assert data["is_active"] is True


def test_get_authorities():
    authority = MagicMock()
    authority.id = 1
    authority.name = "Greater Hyderabad Municipal Corporation"
    authority.code = "GHMC"
    authority.description = "Hyderabad municipal authority"
    authority.is_active = True

    with patch(
        "backend.authority.router.AuthorityService"
    ) as service_class:
        service = service_class.return_value
        service.get_authorities.return_value = [authority]

        response = client.get("/api/authorities")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["id"] == 1
    assert data[0]["code"] == "GHMC"


def test_get_authority():
    authority = MagicMock()
    authority.id = 1
    authority.name = "Greater Hyderabad Municipal Corporation"
    authority.code = "GHMC"
    authority.description = "Hyderabad municipal authority"
    authority.is_active = True

    with patch(
        "backend.authority.router.AuthorityService"
    ) as service_class:
        service = service_class.return_value
        service.get_authority.return_value = authority

        response = client.get("/api/authorities/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Greater Hyderabad Municipal Corporation"


def test_get_authority_not_found():
    with patch(
        "backend.authority.router.AuthorityService"
    ) as service_class:
        service = service_class.return_value
        service.get_authority.return_value = None

        response = client.get("/api/authorities/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Authority not found"


def test_create_authority_validation_error():
    with patch(
        "backend.authority.router.AuthorityService"
    ) as service_class:
        service = service_class.return_value
        service.create_authority.side_effect = ValueError(
            "Authority code already exists"
        )

        response = client.post(
            "/api/authorities",
            json={
                "name": "Test Authority",
                "code": "TEST",
                "description": "Test authority",
            },
        )

    assert response.status_code == 400
    assert response.json()["detail"] == "Authority code already exists"


# ============================================================
# Department API Tests
# ============================================================


def test_create_department():
    department = MagicMock()
    department.id = 1
    department.authority_id = 1
    department.name = "Roads Department"
    department.code = "ROADS"
    department.description = "Road maintenance"
    department.is_active = True

    with patch(
        "backend.authority.router.DepartmentService"
    ) as service_class:
        service = service_class.return_value
        service.create_department.return_value = department

        response = client.post(
            "/api/authorities/1/departments",
            json={
                "authority_id": 1,
                "name": "Roads Department",
                "code": "ROADS",
                "description": "Road maintenance",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["authority_id"] == 1
    assert data["name"] == "Roads Department"


def test_create_department_path_body_mismatch():
    response = client.post(
        "/api/authorities/1/departments",
        json={
            "authority_id": 2,
            "name": "Roads Department",
            "code": "ROADS",
            "description": "Road maintenance",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Authority ID in path and request body must match"
    )


def test_get_departments():
    department = MagicMock()
    department.id = 1
    department.authority_id = 1
    department.name = "Roads Department"
    department.code = "ROADS"
    department.description = None
    department.is_active = True

    with patch(
        "backend.authority.router.DepartmentService"
    ) as service_class:
        service = service_class.return_value
        service.get_departments_by_authority.return_value = [
            department
        ]

        response = client.get(
            "/api/authorities/1/departments"
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["authority_id"] == 1


# ============================================================
# Officer API Tests
# ============================================================


def test_create_officer():
    officer = MagicMock()
    officer.id = 1
    officer.department_id = 1
    officer.name = "Ravi Kumar"
    officer.email = "ravi@example.com"
    officer.phone = "9876543210"
    officer.role = "Officer"
    officer.is_active = True

    with patch(
        "backend.authority.router.OfficerService"
    ) as service_class:
        service = service_class.return_value
        service.create_officer.return_value = officer

        response = client.post(
            "/api/authorities/departments/1/officers",
            json={
                "department_id": 1,
                "name": "Ravi Kumar",
                "email": "ravi@example.com",
                "phone": "9876543210",
                "role": "Officer",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["department_id"] == 1
    assert data["name"] == "Ravi Kumar"


def test_create_officer_path_body_mismatch():
    response = client.post(
        "/api/authorities/departments/1/officers",
        json={
            "department_id": 2,
            "name": "Ravi Kumar",
            "email": "ravi@example.com",
            "phone": "9876543210",
            "role": "Officer",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Department ID in path and request body must match"
    )


def test_get_officers():
    officer = MagicMock()
    officer.id = 1
    officer.department_id = 1
    officer.name = "Ravi Kumar"
    officer.email = "ravi@example.com"
    officer.phone = None
    officer.role = "Officer"
    officer.is_active = True

    with patch(
        "backend.authority.router.OfficerService"
    ) as service_class:
        service = service_class.return_value
        service.get_officers_by_department.return_value = [
            officer
        ]

        response = client.get(
            "/api/authorities/departments/1/officers"
        )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Ravi Kumar"


# ============================================================
# Assignment API Tests
# ============================================================


def test_create_assignment():
    assignment = MagicMock()
    assignment.id = 1
    assignment.complaint_id = 101
    assignment.department_id = 1
    assignment.officer_id = 5
    assignment.assigned_at = "2026-10-02T10:00:00"
    assignment.accepted_at = None
    assignment.completed_at = None
    assignment.notes = "Assigned to officer"

    with patch(
        "backend.authority.router.AssignmentService"
    ) as service_class:
        service = service_class.return_value
        service.create_assignment.return_value = assignment

        response = client.post(
            "/api/authorities/assignments",
            json={
                "complaint_id": 101,
                "department_id": 1,
                "officer_id": 5,
                "notes": "Assigned to officer",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["department_id"] == 1
    assert data["officer_id"] == 5


def test_get_assignment_not_found():
    with patch(
        "backend.authority.router.AssignmentService"
    ) as service_class:
        service = service_class.return_value
        service.get_assignment.return_value = None

        response = client.get(
            "/api/authorities/assignments/999"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Assignment not found"


def test_accept_assignment_not_found():
    with patch(
        "backend.authority.router.AssignmentService"
    ) as service_class:
        service = service_class.return_value
        service.accept_assignment.return_value = None

        response = client.patch(
            "/api/authorities/assignments/999/accept"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Assignment not found"


def test_complete_assignment_not_found():
    with patch(
        "backend.authority.router.AssignmentService"
    ) as service_class:
        service = service_class.return_value
        service.complete_assignment.return_value = None

        response = client.patch(
            "/api/authorities/assignments/999/complete"
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Assignment not found"


# ============================================================
# Status History API Tests
# ============================================================


def test_create_status_history():
    history = MagicMock()
    history.id = 1
    history.complaint_id = 101
    history.old_status = "submitted"
    history.new_status = "assigned"
    history.changed_by = 5
    history.comment = "Assigned to department"
    history.created_at = "2026-10-02T10:00:00"

    with patch(
        "backend.authority.router.StatusHistoryService"
    ) as service_class:
        service = service_class.return_value
        service.create_history.return_value = history

        response = client.post(
            "/api/authorities/complaints/101/status-history",
            json={
                "complaint_id": 101,
                "old_status": "submitted",
                "new_status": "assigned",
                "changed_by": 5,
                "comment": "Assigned to department",
            },
        )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["complaint_id"] == 101
    assert data["old_status"] == "submitted"
    assert data["new_status"] == "assigned"


def test_create_status_history_path_body_mismatch():
    response = client.post(
        "/api/authorities/complaints/101/status-history",
        json={
            "complaint_id": 999,
            "old_status": "submitted",
            "new_status": "assigned",
            "changed_by": 5,
            "comment": "Assigned",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Complaint ID in path and request body must match"
    )


def test_get_status_history_not_found():
    with patch(
        "backend.authority.router.StatusHistoryService"
    ) as service_class:
        service = service_class.return_value
        service.get_history.return_value = None

        response = client.get(
            "/api/authorities/status-history/999"
        )

    assert response.status_code == 404
    assert (
        response.json()["detail"]
        == "Status history record not found"
    )
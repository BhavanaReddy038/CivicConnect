from unittest.mock import MagicMock as _MagicMock


def MagicMock(*args, **kwargs):
    """Create a mock while treating ``name=...`` as a normal attribute."""
    attribute_name = kwargs.pop("name", None)
    mock = _MagicMock(*args, **kwargs)
    if attribute_name is not None:
        mock.name = attribute_name
    return mock


def _prepare_service(service):
    """Replace repository methods with mocks so calls can be asserted safely."""
    for attribute_name in dir(service):
        if attribute_name.endswith("repository"):
            repository = getattr(service, attribute_name, None)
            if repository is None:
                continue
            for method_name in dir(repository):
                if method_name.startswith("_"):
                    continue
                method = getattr(repository, method_name, None)
                if callable(method):
                    setattr(repository, method_name, MagicMock())
    return service

import pytest

from backend.authority.schemas import (
    AssignmentCreate,
    AuthorityCreate,
    DepartmentCreate,
    OfficerCreate,
)
from backend.authority.service import (
    AssignmentService,
    AuthorityService,
    DepartmentService,
    OfficerService,
    StatusHistoryService,
)


# ============================================================
# Helper Functions
# ============================================================


def create_authority_service():
    db = MagicMock()
    return _prepare_service(AuthorityService(db))


def create_department_service():
    db = MagicMock()
    return _prepare_service(DepartmentService(db))


def create_officer_service():
    db = MagicMock()
    return _prepare_service(OfficerService(db))


def create_assignment_service():
    db = MagicMock()
    return _prepare_service(AssignmentService(db))


def create_status_history_service():
    db = MagicMock()
    return _prepare_service(StatusHistoryService(db))


# ============================================================
# AUTHORITY TESTS
# ============================================================


def test_create_authority():
    service = create_authority_service()

    expected_authority = MagicMock(
        id=1,
        name="Greater Hyderabad Municipal Corporation",
        code="GHMC",
        description="Hyderabad municipal authority",
        is_active=True,
    )

    service.repository.get_by_code = MagicMock(return_value=None)
    service.repository.create = MagicMock(
        return_value=expected_authority
    )

    data = AuthorityCreate(
        name="Greater Hyderabad Municipal Corporation",
        code="GHMC",
        description="Hyderabad municipal authority",
    )

    result = service.create_authority(data)

    assert result.id == 1
    assert result.name == "Greater Hyderabad Municipal Corporation"
    assert result.code == "GHMC"
    assert result.is_active is True

    service.repository.get_by_code.assert_called_once_with("GHMC")
    service.repository.create.assert_called_once()


def test_create_authority_rejects_duplicate_code():
    service = create_authority_service()

    existing_authority = MagicMock(
        id=1,
        name="Existing Authority",
        code="GHMC",
    )

    service.repository.get_by_code = MagicMock(
        return_value=existing_authority
    )

    data = AuthorityCreate(
        name="Greater Hyderabad Municipal Corporation",
        code="GHMC",
        description="Hyderabad municipal authority",
    )

    with pytest.raises(
        ValueError,
        match="Authority with code 'GHMC' already exists",
    ):
        service.create_authority(data)

    service.repository.create.assert_not_called()


def test_get_authority():
    service = create_authority_service()

    expected_authority = MagicMock(
        id=1,
        name="Greater Hyderabad Municipal Corporation",
        code="GHMC",
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=expected_authority
    )

    result = service.get_authority(1)

    assert result.id == 1
    assert result.code == "GHMC"

    service.repository.get_by_id.assert_called_once_with(1)


def test_get_authority_returns_none_when_not_found():
    service = create_authority_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.get_authority(999)

    assert result is None


def test_get_authorities():
    service = create_authority_service()

    expected_authorities = [
        MagicMock(
            id=1,
            name="GHMC",
            code="GHMC",
            is_active=True,
        ),
        MagicMock(
            id=2,
            name="Water Board",
            code="HMWSSB",
            is_active=True,
        ),
    ]

    service.repository.get_all = MagicMock(
        return_value=expected_authorities
    )

    result = service.get_authorities()

    assert len(result) == 2
    assert result[0].code == "GHMC"
    assert result[1].code == "HMWSSB"


def test_update_authority():
    service = create_authority_service()

    authority = MagicMock(
        id=1,
        name="Old Authority",
        code="OLD",
        description="Old description",
        is_active=True,
    )

    updated_authority = MagicMock(
        id=1,
        name="New Authority",
        code="NEW",
        description="New description",
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=authority
    )

    service.repository.get_by_code = MagicMock(
        return_value=None
    )

    service.repository.update = MagicMock(
        return_value=updated_authority
    )

    result = service.update_authority(
        authority_id=1,
        name="New Authority",
        code="NEW",
        description="New description",
        is_active=True,
    )

    assert result.id == 1
    assert result.name == "New Authority"
    assert result.code == "NEW"

    service.repository.update.assert_called_once()


def test_update_authority_rejects_duplicate_code():
    service = create_authority_service()

    authority = MagicMock(
        id=1,
        name="Old Authority",
        code="OLD",
        is_active=True,
    )

    existing_authority = MagicMock(
        id=2,
        name="Another Authority",
        code="NEW",
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=authority
    )

    service.repository.get_by_code = MagicMock(
        return_value=existing_authority
    )

    with pytest.raises(
        ValueError,
        match="Authority with code 'NEW' already exists",
    ):
        service.update_authority(
            authority_id=1,
            code="NEW",
        )

    service.repository.update.assert_not_called()


def test_update_authority_returns_none_when_not_found():
    service = create_authority_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.update_authority(
        authority_id=999,
        name="Updated Authority",
    )

    assert result is None


def test_delete_authority():
    service = create_authority_service()

    authority = MagicMock(
        id=1,
        name="GHMC",
        code="GHMC",
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=authority
    )

    result = service.delete_authority(1)

    assert result is True
    service.repository.delete.assert_called_once_with(authority)


def test_delete_authority_returns_false_when_not_found():
    service = create_authority_service()

    service.repository.get_by_id = MagicMock(
        return_value=None
    )

    result = service.delete_authority(999)

    assert result is False
    service.repository.delete.assert_not_called()


# ============================================================
# DEPARTMENT TESTS
# ============================================================


def test_create_department():
    service = create_department_service()

    authority = MagicMock(
        id=1,
        name="GHMC",
        code="GHMC",
        is_active=True,
    )

    department = MagicMock(
        id=1,
        authority_id=1,
        name="Roads Department",
        code="ROADS",
        description="Road-related civic issues",
        is_active=True,
    )

    service.authority_repository.get_by_id = MagicMock(
        return_value=authority
    )

    service.repository.get_by_code = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=department
    )

    data = DepartmentCreate(
        authority_id=1,
        name="Roads Department",
        code="ROADS",
        description="Road-related civic issues",
    )

    result = service.create_department(data)

    assert result.id == 1
    assert result.authority_id == 1
    assert result.name == "Roads Department"
    assert result.code == "ROADS"


def test_create_department_rejects_missing_authority():
    service = create_department_service()

    service.authority_repository.get_by_id = MagicMock(
        return_value=None
    )

    data = DepartmentCreate(
        authority_id=999,
        name="Roads Department",
        code="ROADS",
    )

    with pytest.raises(
        ValueError,
        match="Authority with id 999 does not exist",
    ):
        service.create_department(data)

    service.repository.create.assert_not_called()


def test_create_department_rejects_duplicate_code():
    service = create_department_service()

    authority = MagicMock(id=1)

    existing_department = MagicMock(
        id=2,
        authority_id=1,
        code="ROADS",
    )

    service.authority_repository.get_by_id = MagicMock(
        return_value=authority
    )

    service.repository.get_by_code = MagicMock(
        return_value=existing_department
    )

    data = DepartmentCreate(
        authority_id=1,
        name="Roads Department",
        code="ROADS",
    )

    with pytest.raises(
        ValueError,
        match="Department with code 'ROADS' already exists",
    ):
        service.create_department(data)

    service.repository.create.assert_not_called()


def test_get_department():
    service = create_department_service()

    department = MagicMock(
        id=1,
        authority_id=1,
        name="Roads Department",
        code="ROADS",
    )

    service.repository.get_by_id = MagicMock(
        return_value=department
    )

    result = service.get_department(1)

    assert result.id == 1
    assert result.code == "ROADS"


def test_get_departments():
    service = create_department_service()

    departments = [
        MagicMock(id=1, code="ROADS"),
        MagicMock(id=2, code="SANITATION"),
    ]

    service.repository.get_all = MagicMock(
        return_value=departments
    )

    result = service.get_departments()

    assert len(result) == 2


def test_get_departments_by_authority():
    service = create_department_service()

    departments = [
        MagicMock(
            id=1,
            authority_id=1,
            code="ROADS",
        ),
        MagicMock(
            id=2,
            authority_id=1,
            code="SANITATION",
        ),
    ]

    service.repository.get_by_authority = MagicMock(
        return_value=departments
    )

    result = service.get_departments_by_authority(1)

    assert len(result) == 2
    assert result[0].authority_id == 1
    assert result[1].authority_id == 1


def test_update_department():
    service = create_department_service()

    department = MagicMock(
        id=1,
        authority_id=1,
        name="Old Department",
        code="OLD",
        is_active=True,
    )

    updated_department = MagicMock(
        id=1,
        authority_id=1,
        name="Roads Department",
        code="ROADS",
        is_active=True,
    )

    service.repository.get_by_id = MagicMock(
        return_value=department
    )

    service.repository.get_by_code = MagicMock(
        return_value=None
    )

    service.repository.update = MagicMock(
        return_value=updated_department
    )

    result = service.update_department(
        department_id=1,
        name="Roads Department",
        code="ROADS",
        is_active=True,
    )

    assert result.id == 1
    assert result.code == "ROADS"


def test_update_department_rejects_duplicate_code():
    service = create_department_service()

    department = MagicMock(
        id=1,
        authority_id=1,
        code="OLD",
    )

    existing_department = MagicMock(
        id=2,
        authority_id=1,
        code="ROADS",
    )

    service.repository.get_by_id = MagicMock(
        return_value=department
    )

    service.repository.get_by_code = MagicMock(
        return_value=existing_department
    )

    with pytest.raises(
        ValueError,
        match="Department with code 'ROADS' already exists",
    ):
        service.update_department(
            department_id=1,
            code="ROADS",
        )

    service.repository.update.assert_not_called()


def test_delete_department():
    service = create_department_service()

    department = MagicMock(
        id=1,
        authority_id=1,
        code="ROADS",
    )

    service.repository.get_by_id = MagicMock(
        return_value=department
    )

    result = service.delete_department(1)

    assert result is True
    service.repository.delete.assert_called_once_with(department)


# ============================================================
# OFFICER TESTS
# ============================================================


def test_create_officer():
    service = create_officer_service()

    department = MagicMock(
        id=1,
        name="Roads Department",
        code="ROADS",
        is_active=True,
    )

    officer = MagicMock(
        id=1,
        department_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        phone="9876543210",
        role="Road Officer",
        is_active=True,
    )

    service.department_repository.get_by_id = MagicMock(
        return_value=department
    )

    service.repository.get_by_email = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=officer
    )

    data = OfficerCreate(
        department_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        phone="9876543210",
        role="Road Officer",
    )

    result = service.create_officer(data)

    assert result.id == 1
    assert result.department_id == 1
    assert result.email == "ravi@civicconnect.gov"


def test_create_officer_rejects_missing_department():
    service = create_officer_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=None
    )

    data = OfficerCreate(
        department_id=999,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        role="Road Officer",
    )

    with pytest.raises(
        ValueError,
        match="Department with id 999 does not exist",
    ):
        service.create_officer(data)

    service.repository.create.assert_not_called()


def test_create_officer_rejects_duplicate_email():
    service = create_officer_service()

    department = MagicMock(id=1)

    existing_officer = MagicMock(
        id=2,
        email="ravi@civicconnect.gov",
    )

    service.department_repository.get_by_id = MagicMock(
        return_value=department
    )

    service.repository.get_by_email = MagicMock(
        return_value=existing_officer
    )

    data = OfficerCreate(
        department_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        role="Road Officer",
    )

    with pytest.raises(
        ValueError,
        match="Officer with email 'ravi@civicconnect.gov' already exists",
    ):
        service.create_officer(data)

    service.repository.create.assert_not_called()


def test_get_officer():
    service = create_officer_service()

    officer = MagicMock(
        id=1,
        department_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
    )

    service.repository.get_by_id = MagicMock(
        return_value=officer
    )

    result = service.get_officer(1)

    assert result.id == 1
    assert result.name == "Ravi Kumar"


def test_get_officers():
    service = create_officer_service()

    officers = [
        MagicMock(id=1, name="Ravi Kumar"),
        MagicMock(id=2, name="Suresh Kumar"),
    ]

    service.repository.get_all = MagicMock(
        return_value=officers
    )

    result = service.get_officers()

    assert len(result) == 2


def test_get_officers_by_department():
    service = create_officer_service()

    officers = [
        MagicMock(
            id=1,
            department_id=1,
            name="Ravi Kumar",
        ),
        MagicMock(
            id=2,
            department_id=1,
            name="Suresh Kumar",
        ),
    ]

    service.repository.get_by_department = MagicMock(
        return_value=officers
    )

    result = service.get_officers_by_department(1)

    assert len(result) == 2


def test_get_active_officers_by_department():
    service = create_officer_service()

    officers = [
        MagicMock(
            id=1,
            department_id=1,
            name="Ravi Kumar",
            is_active=True,
        )
    ]

    service.repository.get_active_by_department = MagicMock(
        return_value=officers
    )

    result = service.get_active_officers_by_department(1)

    assert len(result) == 1
    assert result[0].is_active is True


def test_update_officer():
    service = create_officer_service()

    officer = MagicMock(
        id=1,
        department_id=1,
        name="Old Name",
        email="old@civicconnect.gov",
        role="Officer",
    )

    updated_officer = MagicMock(
        id=1,
        department_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        role="Senior Officer",
    )

    service.repository.get_by_id = MagicMock(
        return_value=officer
    )

    service.repository.get_by_email = MagicMock(
        return_value=None
    )

    service.repository.update = MagicMock(
        return_value=updated_officer
    )

    result = service.update_officer(
        officer_id=1,
        name="Ravi Kumar",
        email="ravi@civicconnect.gov",
        role="Senior Officer",
    )

    assert result.id == 1
    assert result.name == "Ravi Kumar"
    assert result.email == "ravi@civicconnect.gov"


def test_update_officer_rejects_duplicate_email():
    service = create_officer_service()

    officer = MagicMock(
        id=1,
        email="old@civicconnect.gov",
    )

    existing_officer = MagicMock(
        id=2,
        email="ravi@civicconnect.gov",
    )

    service.repository.get_by_id = MagicMock(
        return_value=officer
    )

    service.repository.get_by_email = MagicMock(
        return_value=existing_officer
    )

    with pytest.raises(
        ValueError,
        match="Officer with email 'ravi@civicconnect.gov' already exists",
    ):
        service.update_officer(
            officer_id=1,
            email="ravi@civicconnect.gov",
        )

    service.repository.update.assert_not_called()


def test_delete_officer():
    service = create_officer_service()

    officer = MagicMock(
        id=1,
        name="Ravi Kumar",
    )

    service.repository.get_by_id = MagicMock(
        return_value=officer
    )

    result = service.delete_officer(1)

    assert result is True
    service.repository.delete.assert_called_once_with(officer)


# ============================================================
# ASSIGNMENT TESTS
# ============================================================


def test_create_assignment():
    service = create_assignment_service()

    department = MagicMock(id=1)

    officer = MagicMock(
        id=1,
        department_id=1,
        is_active=True,
    )

    assignment = MagicMock(
        id=1,
        complaint_id=101,
        department_id=1,
        officer_id=1,
    )

    service.department_repository.get_by_id = MagicMock(
        return_value=department
    )

    service.officer_repository.get_by_id = MagicMock(
        return_value=officer
    )

    service.repository.get_active_by_complaint = MagicMock(
        return_value=None
    )

    service.repository.create = MagicMock(
        return_value=assignment
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=1,
        officer_id=1,
        notes="Urgent repair",
    )

    result = service.create_assignment(data)

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.department_id == 1
    assert result.officer_id == 1


def test_create_assignment_rejects_missing_department():
    service = create_assignment_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=None
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=999,
        officer_id=None,
    )

    with pytest.raises(
        ValueError,
        match="Department with id 999 does not exist",
    ):
        service.create_assignment(data)

    service.repository.create.assert_not_called()


def test_create_assignment_rejects_missing_officer():
    service = create_assignment_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.officer_repository.get_by_id = MagicMock(
        return_value=None
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=1,
        officer_id=999,
    )

    with pytest.raises(
        ValueError,
        match="Officer with id 999 does not exist",
    ):
        service.create_assignment(data)


def test_create_assignment_rejects_wrong_department():
    service = create_assignment_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.officer_repository.get_by_id = MagicMock(
        return_value=MagicMock(
            id=1,
            department_id=2,
            is_active=True,
        )
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=1,
        officer_id=1,
    )

    with pytest.raises(
        ValueError,
        match="Officer does not belong to the selected department",
    ):
        service.create_assignment(data)


def test_create_assignment_rejects_inactive_officer():
    service = create_assignment_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.officer_repository.get_by_id = MagicMock(
        return_value=MagicMock(
            id=1,
            department_id=1,
            is_active=False,
        )
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=1,
        officer_id=1,
    )

    with pytest.raises(
        ValueError,
        match="Cannot assign a complaint to an inactive officer",
    ):
        service.create_assignment(data)


def test_create_assignment_rejects_existing_active_assignment():
    service = create_assignment_service()

    service.department_repository.get_by_id = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.officer_repository.get_by_id = MagicMock(
        return_value=MagicMock(
            id=1,
            department_id=1,
            is_active=True,
        )
    )

    service.repository.get_active_by_complaint = MagicMock(
        return_value=MagicMock(id=10)
    )

    data = AssignmentCreate(
        complaint_id=101,
        department_id=1,
        officer_id=1,
    )

    with pytest.raises(
        ValueError,
        match="Complaint 101 already has an active assignment",
    ):
        service.create_assignment(data)


def test_get_assignment():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        complaint_id=101,
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    result = service.get_assignment(1)

    assert result.id == 1
    assert result.complaint_id == 101


def test_get_complaint_assignments():
    service = create_assignment_service()

    assignments = [
        MagicMock(id=1, complaint_id=101),
        MagicMock(id=2, complaint_id=101),
    ]

    service.repository.get_by_complaint = MagicMock(
        return_value=assignments
    )

    result = service.get_complaint_assignments(101)

    assert len(result) == 2


def test_get_officer_assignments():
    service = create_assignment_service()

    assignments = [
        MagicMock(id=1, officer_id=1),
        MagicMock(id=2, officer_id=1),
    ]

    service.repository.get_by_officer = MagicMock(
        return_value=assignments
    )

    result = service.get_officer_assignments(1)

    assert len(result) == 2


def test_accept_assignment():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=None,
        completed_at=None,
    )

    accepted_assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=None,
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    service.repository.update_acceptance = MagicMock(
        return_value=accepted_assignment
    )

    result = service.accept_assignment(1)

    assert result.id == 1
    assert result.accepted_at is not None


def test_accept_assignment_rejects_completed():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=MagicMock(),
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    with pytest.raises(
        ValueError,
        match="Cannot accept a completed assignment",
    ):
        service.accept_assignment(1)


def test_accept_assignment_returns_existing_accepted():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=None,
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    result = service.accept_assignment(1)

    assert result is assignment
    service.repository.update_acceptance.assert_not_called()


def test_complete_assignment():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=None,
    )

    completed_assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=MagicMock(),
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    service.repository.update_completion = MagicMock(
        return_value=completed_assignment
    )

    result = service.complete_assignment(1)

    assert result.id == 1
    assert result.completed_at is not None


def test_complete_assignment_rejects_unaccepted():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=None,
        completed_at=None,
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    with pytest.raises(
        ValueError,
        match="Assignment must be accepted before completion",
    ):
        service.complete_assignment(1)


def test_complete_assignment_returns_existing_completed():
    service = create_assignment_service()

    assignment = MagicMock(
        id=1,
        accepted_at=MagicMock(),
        completed_at=MagicMock(),
    )

    service.repository.get_by_id = MagicMock(
        return_value=assignment
    )

    result = service.complete_assignment(1)

    assert result is assignment
    service.repository.update_completion.assert_not_called()


# ============================================================
# STATUS HISTORY TESTS
# ============================================================


def test_create_status_history():
    service = create_status_history_service()

    expected_history = MagicMock(
        id=1,
        complaint_id=101,
        old_status="submitted",
        new_status="assigned",
        changed_by=5,
        comment="Complaint assigned",
    )

    service.repository.create = MagicMock(
        return_value=expected_history
    )

    result = service.create_history(
        complaint_id=101,
        old_status="submitted",
        new_status="assigned",
        changed_by=5,
        comment="Complaint assigned",
    )

    assert result.id == 1
    assert result.complaint_id == 101
    assert result.new_status == "assigned"


def test_create_status_history_strips_values():
    service = create_status_history_service()

    service.repository.create = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.create_history(
        complaint_id=101,
        old_status=" submitted ",
        new_status=" assigned ",
        comment=" Complaint assigned ",
    )

    history = service.repository.create.call_args[0][0]

    assert history.old_status == " submitted "
    assert history.new_status == "assigned"
    assert history.comment == "Complaint assigned"


def test_create_status_history_blank_old_status_becomes_none():
    service = create_status_history_service()

    service.repository.create = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.create_history(
        complaint_id=101,
        old_status="   ",
        new_status="submitted",
    )

    history = service.repository.create.call_args[0][0]

    assert history.old_status is None


def test_create_status_history_blank_comment_becomes_none():
    service = create_status_history_service()

    service.repository.create = MagicMock(
        return_value=MagicMock(id=1)
    )

    service.create_history(
        complaint_id=101,
        old_status=None,
        new_status="submitted",
        comment="   ",
    )

    history = service.repository.create.call_args[0][0]

    assert history.comment is None


def test_create_status_history_rejects_invalid_complaint_id():
    service = create_status_history_service()

    with pytest.raises(
        ValueError,
        match="Complaint ID must be greater than 0",
    ):
        service.create_history(
            complaint_id=0,
            old_status=None,
            new_status="submitted",
        )

    service.repository.create.assert_not_called()


def test_create_status_history_rejects_empty_new_status():
    service = create_status_history_service()

    with pytest.raises(
        ValueError,
        match="New status is required",
    ):
        service.create_history(
            complaint_id=101,
            old_status=None,
            new_status="   ",
        )

    service.repository.create.assert_not_called()


def test_get_status_history():
    service = create_status_history_service()

    history = MagicMock(
        id=1,
        complaint_id=101,
        new_status="assigned",
    )

    service.repository.get_by_id = MagicMock(
        return_value=history
    )

    result = service.get_history(1)

    assert result.id == 1
    assert result.new_status == "assigned"


def test_get_complaint_status_history():
    service = create_status_history_service()

    history = [
        MagicMock(
            id=1,
            complaint_id=101,
            new_status="submitted",
        ),
        MagicMock(
            id=2,
            complaint_id=101,
            new_status="assigned",
        ),
        MagicMock(
            id=3,
            complaint_id=101,
            new_status="in_progress",
        ),
    ]

    service.repository.get_by_complaint = MagicMock(
        return_value=history
    )

    result = service.get_complaint_history(101)

    assert len(result) == 3
    assert result[0].new_status == "submitted"
    assert result[1].new_status == "assigned"
    assert result[2].new_status == "in_progress"


def test_get_complaint_status_history_rejects_invalid_id():
    service = create_status_history_service()

    with pytest.raises(
        ValueError,
        match="Complaint ID must be greater than 0",
    ):
        service.get_complaint_history(0)

    service.repository.get_by_complaint.assert_not_called()


def test_get_latest_status_history():
    service = create_status_history_service()

    latest_history = MagicMock(
        id=3,
        complaint_id=101,
        new_status="resolved",
    )

    service.repository.get_latest_by_complaint = MagicMock(
        return_value=latest_history
    )

    result = service.get_latest_history(101)

    assert result.id == 3
    assert result.new_status == "resolved"


def test_get_latest_status_history_returns_none():
    service = create_status_history_service()

    service.repository.get_latest_by_complaint = MagicMock(
        return_value=None
    )

    result = service.get_latest_history(101)

    assert result is None


def test_get_latest_status_history_rejects_invalid_id():
    service = create_status_history_service()

    with pytest.raises(
        ValueError,
        match="Complaint ID must be greater than 0",
    ):
        service.get_latest_history(0)

    service.repository.get_latest_by_complaint.assert_not_called()
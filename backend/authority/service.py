from datetime import datetime

from sqlalchemy.orm import Session

from database.models.authority import Authority
from database.models.department import Department
from database.models.officer import Officer
from database.models.assignment import Assignment
from database.models.complaint_status_history import ComplaintStatusHistory

from backend.authority.repository import (
    AssignmentRepository,
    AuthorityRepository,
    DepartmentRepository,
    OfficerRepository,
    StatusHistoryRepository,
)

from backend.authority.schemas import (
    AuthorityCreate,
    DepartmentCreate,
    OfficerCreate,
    AssignmentCreate,
)


# =========================
# Authority Service
# =========================

class AuthorityService:
    def __init__(self, db: Session):
        self.repository = AuthorityRepository(db)

    def create_authority(
        self,
        data: AuthorityCreate,
    ) -> Authority:
        existing_authority = self.repository.get_by_code(data.code)

        if existing_authority:
            raise ValueError(
                f"Authority with code '{data.code}' already exists"
            )

        authority = Authority(
            name=data.name,
            code=data.code,
            description=data.description,
        )

        return self.repository.create(authority)

    def get_authority(
        self,
        authority_id: int,
    ) -> Authority | None:
        return self.repository.get_by_id(authority_id)

    def get_authorities(self) -> list[Authority]:
        return self.repository.get_all()

    def update_authority(
        self,
        authority_id: int,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Authority | None:
        authority = self.repository.get_by_id(authority_id)

        if authority is None:
            return None

        if code is not None and code != authority.code:
            existing_authority = self.repository.get_by_code(code)

            if existing_authority:
                raise ValueError(
                    f"Authority with code '{code}' already exists"
                )

        return self.repository.update(
            authority=authority,
            name=name,
            code=code,
            description=description,
            is_active=is_active,
        )

    def delete_authority(
        self,
        authority_id: int,
    ) -> bool:
        authority = self.repository.get_by_id(authority_id)

        if authority is None:
            return False

        self.repository.delete(authority)

        return True


# =========================
# Department Service
# =========================

class DepartmentService:
    def __init__(self, db: Session):
        self.repository = DepartmentRepository(db)
        self.authority_repository = AuthorityRepository(db)

    def create_department(
        self,
        data: DepartmentCreate,
    ) -> Department:
        authority = self.authority_repository.get_by_id(
            data.authority_id
        )

        if authority is None:
            raise ValueError(
                f"Authority with id {data.authority_id} does not exist"
            )

        existing_department = self.repository.get_by_code(data.code)

        if existing_department:
            raise ValueError(
                f"Department with code '{data.code}' already exists"
            )

        department = Department(
            authority_id=data.authority_id,
            name=data.name,
            code=data.code,
            description=data.description,
        )

        return self.repository.create(department)

    def get_department(
        self,
        department_id: int,
    ) -> Department | None:
        return self.repository.get_by_id(department_id)

    def get_departments(self) -> list[Department]:
        return self.repository.get_all()

    def get_departments_by_authority(
        self,
        authority_id: int,
    ) -> list[Department]:
        return self.repository.get_by_authority(authority_id)

    def update_department(
        self,
        department_id: int,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Department | None:
        department = self.repository.get_by_id(department_id)

        if department is None:
            return None

        if code is not None and code != department.code:
            existing_department = self.repository.get_by_code(code)

            if existing_department:
                raise ValueError(
                    f"Department with code '{code}' already exists"
                )

        return self.repository.update(
            department=department,
            name=name,
            code=code,
            description=description,
            is_active=is_active,
        )

    def delete_department(
        self,
        department_id: int,
    ) -> bool:
        department = self.repository.get_by_id(department_id)

        if department is None:
            return False

        self.repository.delete(department)

        return True


# =========================
# Officer Service
# =========================

class OfficerService:
    def __init__(self, db: Session):
        self.repository = OfficerRepository(db)
        self.department_repository = DepartmentRepository(db)

    def create_officer(
        self,
        data: OfficerCreate,
    ) -> Officer:
        department = self.department_repository.get_by_id(
            data.department_id
        )

        if department is None:
            raise ValueError(
                f"Department with id {data.department_id} does not exist"
            )

        existing_officer = self.repository.get_by_email(data.email)

        if existing_officer:
            raise ValueError(
                f"Officer with email '{data.email}' already exists"
            )

        officer = Officer(
            department_id=data.department_id,
            name=data.name,
            email=data.email,
            phone=data.phone,
            role=data.role,
        )

        return self.repository.create(officer)

    def get_officer(
        self,
        officer_id: int,
    ) -> Officer | None:
        return self.repository.get_by_id(officer_id)

    def get_officers(self) -> list[Officer]:
        return self.repository.get_all()

    def get_officers_by_department(
        self,
        department_id: int,
    ) -> list[Officer]:
        return self.repository.get_by_department(
            department_id
        )

    def get_active_officers_by_department(
        self,
        department_id: int,
    ) -> list[Officer]:
        return self.repository.get_active_by_department(
            department_id
        )

    def update_officer(
        self,
        officer_id: int,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ) -> Officer | None:
        officer = self.repository.get_by_id(officer_id)

        if officer is None:
            return None

        if email is not None and email != officer.email:
            existing_officer = self.repository.get_by_email(email)

            if existing_officer:
                raise ValueError(
                    f"Officer with email '{email}' already exists"
                )

        return self.repository.update(
            officer=officer,
            name=name,
            email=email,
            phone=phone,
            role=role,
            is_active=is_active,
        )

    def delete_officer(
        self,
        officer_id: int,
    ) -> bool:
        officer = self.repository.get_by_id(officer_id)

        if officer is None:
            return False

        self.repository.delete(officer)

        return True


# =========================
# Assignment Service
# =========================

class AssignmentService:
    def __init__(self, db: Session):
        self.repository = AssignmentRepository(db)
        self.department_repository = DepartmentRepository(db)
        self.officer_repository = OfficerRepository(db)

    def create_assignment(
        self,
        data: AssignmentCreate,
    ) -> Assignment:
        department = self.department_repository.get_by_id(
            data.department_id
        )

        if department is None:
            raise ValueError(
                f"Department with id {data.department_id} does not exist"
            )

        if data.officer_id is not None:
            officer = self.officer_repository.get_by_id(
                data.officer_id
            )

            if officer is None:
                raise ValueError(
                    f"Officer with id {data.officer_id} does not exist"
                )

            if officer.department_id != data.department_id:
                raise ValueError(
                    "Officer does not belong to the selected department"
                )

            if not officer.is_active:
                raise ValueError(
                    "Cannot assign a complaint to an inactive officer"
                )

        active_assignment = (
            self.repository.get_active_by_complaint(
                data.complaint_id
            )
        )

        if active_assignment:
            raise ValueError(
                f"Complaint {data.complaint_id} already has "
                "an active assignment"
            )

        assignment = Assignment(
            complaint_id=data.complaint_id,
            department_id=data.department_id,
            officer_id=data.officer_id,
            notes=data.notes,
            assigned_at=datetime.utcnow(),
        )

        return self.repository.create(assignment)

    def get_assignment(
        self,
        assignment_id: int,
    ) -> Assignment | None:
        return self.repository.get_by_id(assignment_id)

    def get_complaint_assignments(
        self,
        complaint_id: int,
    ) -> list[Assignment]:
        return self.repository.get_by_complaint(
            complaint_id
        )

    def get_officer_assignments(
        self,
        officer_id: int,
    ) -> list[Assignment]:
        return self.repository.get_by_officer(
            officer_id
        )

    def accept_assignment(
        self,
        assignment_id: int,
    ) -> Assignment | None:
        assignment = self.repository.get_by_id(
            assignment_id
        )

        if assignment is None:
            return None

        if assignment.completed_at is not None:
            raise ValueError(
                "Cannot accept a completed assignment"
            )

        if assignment.accepted_at is not None:
            return assignment

        return self.repository.update_acceptance(
            assignment=assignment,
            accepted_at=datetime.utcnow(),
        )

    def complete_assignment(
        self,
        assignment_id: int,
    ) -> Assignment | None:
        assignment = self.repository.get_by_id(
            assignment_id
        )

        if assignment is None:
            return None

        if assignment.completed_at is not None:
            return assignment

        if assignment.accepted_at is None:
            raise ValueError(
                "Assignment must be accepted before completion"
            )

        return self.repository.update_completion(
            assignment=assignment,
            completed_at=datetime.utcnow(),
        )


# =========================
# Status History Service
# =========================

class StatusHistoryService:
    def __init__(self, db: Session):
        self.repository = StatusHistoryRepository(db)

    def create_history(
        self,
        complaint_id: int,
        old_status: str | None,
        new_status: str,
        changed_by: int | None = None,
        comment: str | None = None,
    ) -> ComplaintStatusHistory:
        if complaint_id <= 0:
            raise ValueError(
                "Complaint ID must be greater than 0"
            )

        if not new_status.strip():
            raise ValueError(
                "New status is required"
            )

        if old_status is not None and not old_status.strip():
            old_status = None

        if comment is not None and not comment.strip():
            comment = None

        history = ComplaintStatusHistory(
            complaint_id=complaint_id,
            old_status=old_status,
            new_status=new_status.strip(),
            changed_by=changed_by,
            comment=comment.strip() if comment else None,
        )

        return self.repository.create(history)

    def get_history(
        self,
        history_id: int,
    ) -> ComplaintStatusHistory | None:
        return self.repository.get_by_id(history_id)

    def get_complaint_history(
        self,
        complaint_id: int,
    ) -> list[ComplaintStatusHistory]:
        if complaint_id <= 0:
            raise ValueError(
                "Complaint ID must be greater than 0"
            )

        return self.repository.get_by_complaint(
            complaint_id
        )

    def get_latest_history(
        self,
        complaint_id: int,
    ) -> ComplaintStatusHistory | None:
        if complaint_id <= 0:
            raise ValueError(
                "Complaint ID must be greater than 0"
            )

        return self.repository.get_latest_by_complaint(
            complaint_id
        )
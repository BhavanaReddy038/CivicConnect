from sqlalchemy import select
from sqlalchemy.orm import Session

from database.models.authority import Authority
from database.models.department import Department
from database.models.officer import Officer
from database.models.assignment import Assignment
from database.models.complaint_status_history import ComplaintStatusHistory


# =========================
# Authority Repository
# =========================

class AuthorityRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, authority: Authority) -> Authority:
        self.db.add(authority)
        self.db.commit()
        self.db.refresh(authority)

        return authority

    def get_by_id(self, authority_id: int) -> Authority | None:
        statement = select(Authority).where(
            Authority.id == authority_id
        )

        return self.db.scalar(statement)

    def get_by_code(self, code: str) -> Authority | None:
        statement = select(Authority).where(
            Authority.code == code
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Authority]:
        statement = select(Authority).order_by(Authority.id)

        return list(self.db.scalars(statement).all())

    def update(
        self,
        authority: Authority,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Authority:
        if name is not None:
            authority.name = name

        if code is not None:
            authority.code = code

        if description is not None:
            authority.description = description

        if is_active is not None:
            authority.is_active = is_active

        self.db.commit()
        self.db.refresh(authority)

        return authority

    def delete(self, authority: Authority) -> None:
        self.db.delete(authority)
        self.db.commit()


# =========================
# Department Repository
# =========================

class DepartmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, department: Department) -> Department:
        self.db.add(department)
        self.db.commit()
        self.db.refresh(department)

        return department

    def get_by_id(self, department_id: int) -> Department | None:
        statement = select(Department).where(
            Department.id == department_id
        )

        return self.db.scalar(statement)

    def get_by_code(self, code: str) -> Department | None:
        statement = select(Department).where(
            Department.code == code
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Department]:
        statement = select(Department).order_by(Department.id)

        return list(self.db.scalars(statement).all())

    def get_by_authority(
        self,
        authority_id: int,
    ) -> list[Department]:
        statement = (
            select(Department)
            .where(Department.authority_id == authority_id)
            .order_by(Department.id)
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        department: Department,
        name: str | None = None,
        code: str | None = None,
        description: str | None = None,
        is_active: bool | None = None,
    ) -> Department:
        if name is not None:
            department.name = name

        if code is not None:
            department.code = code

        if description is not None:
            department.description = description

        if is_active is not None:
            department.is_active = is_active

        self.db.commit()
        self.db.refresh(department)

        return department

    def delete(self, department: Department) -> None:
        self.db.delete(department)
        self.db.commit()


# =========================
# Officer Repository
# =========================

class OfficerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, officer: Officer) -> Officer:
        self.db.add(officer)
        self.db.commit()
        self.db.refresh(officer)

        return officer

    def get_by_id(self, officer_id: int) -> Officer | None:
        statement = select(Officer).where(
            Officer.id == officer_id
        )

        return self.db.scalar(statement)

    def get_by_email(self, email: str) -> Officer | None:
        statement = select(Officer).where(
            Officer.email == email
        )

        return self.db.scalar(statement)

    def get_all(self) -> list[Officer]:
        statement = select(Officer).order_by(Officer.id)

        return list(self.db.scalars(statement).all())

    def get_by_department(
        self,
        department_id: int,
    ) -> list[Officer]:
        statement = (
            select(Officer)
            .where(Officer.department_id == department_id)
            .order_by(Officer.id)
        )

        return list(self.db.scalars(statement).all())

    def get_active_by_department(
        self,
        department_id: int,
    ) -> list[Officer]:
        statement = (
            select(Officer)
            .where(
                Officer.department_id == department_id,
                Officer.is_active.is_(True),
            )
            .order_by(Officer.id)
        )

        return list(self.db.scalars(statement).all())

    def update(
        self,
        officer: Officer,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        role: str | None = None,
        is_active: bool | None = None,
    ) -> Officer:
        if name is not None:
            officer.name = name

        if email is not None:
            officer.email = email

        if phone is not None:
            officer.phone = phone

        if role is not None:
            officer.role = role

        if is_active is not None:
            officer.is_active = is_active

        self.db.commit()
        self.db.refresh(officer)

        return officer

    def delete(self, officer: Officer) -> None:
        self.db.delete(officer)
        self.db.commit()


# =========================
# Assignment Repository
# =========================

class AssignmentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        assignment: Assignment,
    ) -> Assignment:
        self.db.add(assignment)
        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def get_by_id(
        self,
        assignment_id: int,
    ) -> Assignment | None:
        statement = select(Assignment).where(
            Assignment.id == assignment_id
        )

        return self.db.scalar(statement)

    def get_by_complaint(
        self,
        complaint_id: int,
    ) -> list[Assignment]:
        statement = (
            select(Assignment)
            .where(
                Assignment.complaint_id == complaint_id
            )
            .order_by(Assignment.assigned_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def get_active_by_complaint(
        self,
        complaint_id: int,
    ) -> Assignment | None:
        statement = select(Assignment).where(
            Assignment.complaint_id == complaint_id,
            Assignment.completed_at.is_(None),
        )

        return self.db.scalar(statement)

    def get_by_officer(
        self,
        officer_id: int,
    ) -> list[Assignment]:
        statement = (
            select(Assignment)
            .where(
                Assignment.officer_id == officer_id
            )
            .order_by(Assignment.assigned_at.desc())
        )

        return list(self.db.scalars(statement).all())

    def update_acceptance(
        self,
        assignment: Assignment,
        accepted_at,
    ) -> Assignment:
        assignment.accepted_at = accepted_at

        self.db.commit()
        self.db.refresh(assignment)

        return assignment

    def update_completion(
        self,
        assignment: Assignment,
        completed_at,
    ) -> Assignment:
        assignment.completed_at = completed_at

        self.db.commit()
        self.db.refresh(assignment)

        return assignment


# =========================
# Status History Repository
# =========================

class StatusHistoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        history: ComplaintStatusHistory,
    ) -> ComplaintStatusHistory:
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)

        return history

    def get_by_id(
        self,
        history_id: int,
    ) -> ComplaintStatusHistory | None:
        statement = select(ComplaintStatusHistory).where(
            ComplaintStatusHistory.id == history_id
        )

        return self.db.scalar(statement)

    def get_by_complaint(
        self,
        complaint_id: int,
    ) -> list[ComplaintStatusHistory]:
        statement = (
            select(ComplaintStatusHistory)
            .where(
                ComplaintStatusHistory.complaint_id == complaint_id
            )
            .order_by(
                ComplaintStatusHistory.created_at.asc()
            )
        )

        return list(self.db.scalars(statement).all())

    def get_latest_by_complaint(
        self,
        complaint_id: int,
    ) -> ComplaintStatusHistory | None:
        statement = (
            select(ComplaintStatusHistory)
            .where(
                ComplaintStatusHistory.complaint_id == complaint_id
            )
            .order_by(
                ComplaintStatusHistory.created_at.desc()
            )
            .limit(1)
        )

        return self.db.scalar(statement)
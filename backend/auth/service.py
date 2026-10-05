from sqlalchemy.orm import Session

from backend.auth.repository import AuthRepository
from backend.auth.schemas import UserRegister
from backend.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from database.models.user import User


class AuthService:

    def __init__(self):
        self.repository = AuthRepository()

    def register(
        self,
        db: Session,
        data: UserRegister,
    ) -> User:

        # Check whether email already exists
        existing_user = self.repository.get_user_by_email(
            db,
            data.email,
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        # Hash password
        password_hash = hash_password(
            data.password
        )

        # Create database user
        user = User(
            name=data.name,
            email=data.email,
            password_hash=password_hash,
            role=data.role,
            is_verified=False,
            is_active=True,
        )

        return self.repository.create_user(
            db,
            user,
        )

    def login(
        self,
        db: Session,
        email: str,
        password: str,
    ):

        user = self.repository.get_user_by_email(
            db,
            email,
        )

        if not user:
            raise ValueError(
                "Invalid email or password"
            )

        if not user.is_active:
            raise ValueError(
                "User account is inactive"
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            user_id=user.id,
            role=user.role.value,
        )

        return access_token, user

    def get_user_by_id(
        self,
        db: Session,
        user_id: int,
    ) -> User | None:

        return self.repository.get_user_by_id(
            db,
            user_id,
        )
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from database import models  # noqa: E402, F401
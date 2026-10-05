from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from geoalchemy2 import Geometry

from database.base import Base


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    point = mapped_column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=True,
    )

    complaints = relationship(
        "Complaint",
        back_populates="location",
    )
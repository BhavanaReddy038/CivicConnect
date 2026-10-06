from logging.config import fileConfig
import os
import sys

from dotenv import load_dotenv
from sqlalchemy import engine_from_config
from sqlalchemy import pool

# pyrefly: ignore [missing-import]
from alembic import context


# ------------------------------------------------------------
# Add project root to Python path
# ------------------------------------------------------------

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
)


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv()


# ------------------------------------------------------------
# Alembic configuration
# ------------------------------------------------------------

config = context.config


# ------------------------------------------------------------
# Load DATABASE_URL from .env
# ------------------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set in the .env file"
    )


# ------------------------------------------------------------
# Configure Alembic logging
# ------------------------------------------------------------

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# ------------------------------------------------------------
# Import SQLAlchemy Base and models
# ------------------------------------------------------------

from database.base import Base  # noqa: E402
from database import models  # noqa: E402, F401


# ------------------------------------------------------------
# SQLAlchemy metadata
# ------------------------------------------------------------

target_metadata = Base.metadata


# ------------------------------------------------------------
# Offline migration mode
# ------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.
    """

    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ------------------------------------------------------------
# Online migration mode
# ------------------------------------------------------------

def run_migrations_online() -> None:
    """
    Run migrations using an active database connection.
    """

    configuration = config.get_section(
        config.config_ini_section,
        {}
    )

    configuration["sqlalchemy.url"] = DATABASE_URL

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


# ------------------------------------------------------------
# Run the appropriate migration mode
# ------------------------------------------------------------

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
"""Create Authority and SLA tables.

Revision ID: 20261005_01
Revises: b03d35ce7368
Create Date: 2026-10-05
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20261005_01"
down_revision = "b03d35ce7368"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create Authority and SLA related tables."""

    # ============================================================
    # Authorities
    # ============================================================

    op.create_table(
        "authorities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("code"),
    )

    op.create_index(
        "ix_authorities_id",
        "authorities",
        ["id"],
        unique=False,
    )


    # ============================================================
    # Departments
    # ============================================================

    op.create_table(
        "departments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("authority_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("code", sa.String(length=50), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(
            ["authority_id"],
            ["authorities.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_departments_id",
        "departments",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_departments_authority_id",
        "departments",
        ["authority_id"],
        unique=False,
    )


    # ============================================================
    # Officers
    # ============================================================

    op.create_table(
        "officers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=20), nullable=True),
        sa.Column("role", sa.String(length=100), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

    op.create_index(
        "ix_officers_id",
        "officers",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_officers_department_id",
        "officers",
        ["department_id"],
        unique=False,
    )


    # ============================================================
    # Assignments
    # ============================================================

    op.create_table(
        "assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("officer_id", sa.Integer(), nullable=True),
        sa.Column("assigned_at", sa.DateTime(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.ForeignKeyConstraint(
            ["officer_id"],
            ["officers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_assignments_id",
        "assignments",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_assignments_complaint_id",
        "assignments",
        ["complaint_id"],
        unique=False,
    )

    op.create_index(
        "ix_assignments_department_id",
        "assignments",
        ["department_id"],
        unique=False,
    )

    op.create_index(
        "ix_assignments_officer_id",
        "assignments",
        ["officer_id"],
        unique=False,
    )


    # ============================================================
    # Complaint Status History
    # ============================================================

    op.create_table(
        "complaint_status_history",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("old_status", sa.String(length=50), nullable=True),
        sa.Column("new_status", sa.String(length=50), nullable=False),
        sa.Column("changed_by", sa.Integer(), nullable=True),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),
        sa.ForeignKeyConstraint(
            ["changed_by"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_complaint_status_history_id",
        "complaint_status_history",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_complaint_status_history_complaint_id",
        "complaint_status_history",
        ["complaint_id"],
        unique=False,
    )

    op.create_index(
        "ix_complaint_status_history_changed_by",
        "complaint_status_history",
        ["changed_by"],
        unique=False,
    )


    # ============================================================
    # SLA Rules
    # ============================================================

    op.create_table(
        "sla_rules",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("department_id", sa.Integer(), nullable=False),
        sa.Column("priority", sa.String(length=50), nullable=False),
        sa.Column("target_hours", sa.Integer(), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
        sa.ForeignKeyConstraint(
            ["department_id"],
            ["departments.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_sla_rules_id",
        "sla_rules",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_sla_rules_department_id",
        "sla_rules",
        ["department_id"],
        unique=False,
    )


    # ============================================================
    # SLA Tracking
    # ============================================================

    op.create_table(
        "sla_tracking",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("target_hours", sa.Integer(), nullable=False),
        sa.Column("due_at", sa.DateTime(), nullable=False),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="active",
        ),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_sla_tracking_id",
        "sla_tracking",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_sla_tracking_complaint_id",
        "sla_tracking",
        ["complaint_id"],
        unique=False,
    )


    # ============================================================
    # Escalations
    # ============================================================

    op.create_table(
        "escalations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),
        sa.Column("from_level", sa.String(length=50), nullable=False),
        sa.Column("to_level", sa.String(length=50), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("triggered_at", sa.DateTime(), nullable=False),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            nullable=False,
            server_default="active",
        ),
        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_escalations_id",
        "escalations",
        ["id"],
        unique=False,
    )

    op.create_index(
        "ix_escalations_complaint_id",
        "escalations",
        ["complaint_id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove Authority and SLA related tables."""

    # Drop in reverse dependency order.

    op.drop_index(
        "ix_escalations_complaint_id",
        table_name="escalations",
    )
    op.drop_index(
        "ix_escalations_id",
        table_name="escalations",
    )
    op.drop_table("escalations")

    op.drop_index(
        "ix_sla_tracking_complaint_id",
        table_name="sla_tracking",
    )
    op.drop_index(
        "ix_sla_tracking_id",
        table_name="sla_tracking",
    )
    op.drop_table("sla_tracking")

    op.drop_index(
        "ix_sla_rules_department_id",
        table_name="sla_rules",
    )
    op.drop_index(
        "ix_sla_rules_id",
        table_name="sla_rules",
    )
    op.drop_table("sla_rules")

    op.drop_index(
        "ix_complaint_status_history_changed_by",
        table_name="complaint_status_history",
    )
    op.drop_index(
        "ix_complaint_status_history_complaint_id",
        table_name="complaint_status_history",
    )
    op.drop_index(
        "ix_complaint_status_history_id",
        table_name="complaint_status_history",
    )
    op.drop_table("complaint_status_history")

    op.drop_index(
        "ix_assignments_officer_id",
        table_name="assignments",
    )
    op.drop_index(
        "ix_assignments_department_id",
        table_name="assignments",
    )
    op.drop_index(
        "ix_assignments_complaint_id",
        table_name="assignments",
    )
    op.drop_index(
        "ix_assignments_id",
        table_name="assignments",
    )
    op.drop_table("assignments")

    op.drop_index(
        "ix_officers_department_id",
        table_name="officers",
    )
    op.drop_index(
        "ix_officers_id",
        table_name="officers",
    )
    op.drop_table("officers")

    op.drop_index(
        "ix_departments_authority_id",
        table_name="departments",
    )
    op.drop_index(
        "ix_departments_id",
        table_name="departments",
    )
    op.drop_table("departments")

    op.drop_index(
        "ix_authorities_id",
        table_name="authorities",



        
    )
    op.drop_table("authorities")
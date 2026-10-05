"""initial civicconnect models

Revision ID: b03d35ce7368
Revises:
Create Date: 2026-10-05 09:52:53.295283

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision: str = "b03d35ce7368"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ---------------------------------------------------------
    # ISSUE CATEGORIES
    # ---------------------------------------------------------
    op.create_table(
        "issue_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("department_id", sa.Integer(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )

    op.create_index(
        op.f("ix_issue_categories_id"),
        "issue_categories",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # LOCATIONS
    # ---------------------------------------------------------
    op.create_table(
        "locations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),

        # IMPORTANT:
        # spatial_index=False prevents GeoAlchemy2 from
        # automatically creating idx_locations_point here.
        # We create the index explicitly below.
        sa.Column(
            "point",
            geoalchemy2.types.Geometry(
                geometry_type="POINT",
                srid=4326,
                dimension=2,
                from_text="ST_GeomFromEWKT",
                name="geometry",
                spatial_index=False,
            ),
            nullable=True,
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    # Explicit PostGIS spatial index
    op.create_index(
        "idx_locations_point",
        "locations",
        ["point"],
        unique=False,
        postgresql_using="gist",
    )

    op.create_index(
        op.f("ix_locations_id"),
        "locations",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # USERS
    # ---------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),

        sa.Column(
            "role",
            sa.Enum(
                "CITIZEN",
                "OFFICER",
                "AUTHORITY_ADMIN",
                "SUPER_ADMIN",
                name="userrole",
            ),
            nullable=False,
        ),

        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )

    op.create_index(
        op.f("ix_users_id"),
        "users",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # COMPLAINTS
    # ---------------------------------------------------------
    op.create_table(
        "complaints",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("location_id", sa.Integer(), nullable=True),

        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),

        sa.Column(
            "affected_people",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "status",
            sa.Enum(
                "SUBMITTED",
                "UNDER_REVIEW",
                "ASSIGNED",
                "IN_PROGRESS",
                "RESOLVED",
                "REJECTED",
                name="complaintstatus",
            ),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["category_id"],
            ["issue_categories.id"],
        ),

        sa.ForeignKeyConstraint(
            ["location_id"],
            ["locations.id"],
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_complaints_category_id"),
        "complaints",
        ["category_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_complaints_id"),
        "complaints",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_complaints_location_id"),
        "complaints",
        ["location_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_complaints_user_id"),
        "complaints",
        ["user_id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------
    op.create_table(
        "ai_analysis",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("complaint_id", sa.Integer(), nullable=False),

        sa.Column(
            "predicted_category",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "severity",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "severity_score",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "summary",
            sa.Text(),
            nullable=True,
        ),

        sa.Column(
            "confidence",
            sa.Float(),
            nullable=True,
        ),

        sa.Column(
            "extracted_data",
            sa.JSON(),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint("complaint_id"),
    )

    op.create_index(
        op.f("ix_ai_analysis_id"),
        "ai_analysis",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # COMPLAINT MEDIA
    # ---------------------------------------------------------
    op.create_table(
        "complaint_media",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "complaint_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "media_type",
            sa.Enum(
                "IMAGE",
                "VIDEO",
                "AUDIO",
                name="mediatype",
            ),
            nullable=False,
        ),

        sa.Column(
            "file_url",
            sa.String(length=1000),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_complaint_media_id"),
        "complaint_media",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # COMPLAINT POSTS
    # ---------------------------------------------------------
    op.create_table(
        "complaint_posts",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "complaint_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "is_visible",
            sa.Boolean(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["complaint_id"],
            ["complaints.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),

        sa.UniqueConstraint("complaint_id"),
    )

    op.create_index(
        op.f("ix_complaint_posts_id"),
        "complaint_posts",
        ["id"],
        unique=False,
    )

    # ---------------------------------------------------------
    # POST COMMENTS
    # ---------------------------------------------------------
    op.create_table(
        "post_comments",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "post_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["post_id"],
            ["complaint_posts.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    # ---------------------------------------------------------
    # POST MEDIA
    # ---------------------------------------------------------
    op.create_table(
        "post_media",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "post_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "media_type",
            sa.Enum(
                "IMAGE",
                "VIDEO",
                name="postmediatype",
            ),
            nullable=False,
        ),

        sa.Column(
            "file_url",
            sa.String(length=1000),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["post_id"],
            ["complaint_posts.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),
    )

    # ---------------------------------------------------------
    # POST VOTES
    # ---------------------------------------------------------
    op.create_table(
        "post_votes",
        sa.Column("id", sa.Integer(), nullable=False),

        sa.Column(
            "post_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["post_id"],
            ["complaint_posts.id"],
            ondelete="CASCADE",
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            ondelete="CASCADE",
        ),

        sa.PrimaryKeyConstraint("id"),

        # One user can vote only once on a post
        sa.UniqueConstraint(
            "post_id",
            "user_id",
            name="uq_post_user_vote",
        ),
    )


def downgrade() -> None:

    # ---------------------------------------------------------
    # POST VOTES
    # ---------------------------------------------------------
    op.drop_table("post_votes")

    # ---------------------------------------------------------
    # POST MEDIA
    # ---------------------------------------------------------
    op.drop_table("post_media")

    # ---------------------------------------------------------
    # POST COMMENTS
    # ---------------------------------------------------------
    op.drop_table("post_comments")

    # ---------------------------------------------------------
    # COMPLAINT POSTS
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_complaint_posts_id"),
        table_name="complaint_posts",
    )

    op.drop_table("complaint_posts")

    # ---------------------------------------------------------
    # COMPLAINT MEDIA
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_complaint_media_id"),
        table_name="complaint_media",
    )

    op.drop_table("complaint_media")

    # ---------------------------------------------------------
    # AI ANALYSIS
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_ai_analysis_id"),
        table_name="ai_analysis",
    )

    op.drop_table("ai_analysis")

    # ---------------------------------------------------------
    # COMPLAINTS
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_complaints_user_id"),
        table_name="complaints",
    )

    op.drop_index(
        op.f("ix_complaints_location_id"),
        table_name="complaints",
    )

    op.drop_index(
        op.f("ix_complaints_id"),
        table_name="complaints",
    )

    op.drop_index(
        op.f("ix_complaints_category_id"),
        table_name="complaints",
    )

    op.drop_table("complaints")

    # ---------------------------------------------------------
    # USERS
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_users_id"),
        table_name="users",
    )

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )

    op.drop_table("users")

    # ---------------------------------------------------------
    # LOCATIONS
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_locations_id"),
        table_name="locations",
    )

    op.drop_index(
        "idx_locations_point",
        table_name="locations",
        postgresql_using="gist",
    )

    op.drop_table("locations")

    # ---------------------------------------------------------
    # ISSUE CATEGORIES
    # ---------------------------------------------------------
    op.drop_index(
        op.f("ix_issue_categories_id"),
        table_name="issue_categories",
    )

    op.drop_table("issue_categories")
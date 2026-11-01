"""add student id format check

Revision ID: d22f5723e1d0
Revises: 97c40e14454a
Create Date: 2026-11-01 23:17:06.667311

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd22f5723e1d0'
down_revision = '97c40e14454a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        "ck_users_student_id", "users", "student_id ~ '^[0-9]{4}-[0-9]{4}$'"
    )


def downgrade():
    op.drop_constraint("ck_users_student_id", "users", type_="check")

"""create analytics table

Revision ID: 02dddb6bb03d
Revises: 79f05cc45ebe
Create Date: 2021-06-28 13:13:21.264245

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02dddb6bb03d'
down_revision = '79f05cc45ebe'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True, unique=True),
        sa.Column("hashed_password", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_user_full_name"), "users", ["full_name"], unique=False)
    op.create_index(op.f("ix_user_id"), "users", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_user_id"), table_name="users")
    op.drop_index(op.f("ix_user_full_name"), table_name="users")
    op.drop_index(op.f("ix_user_email"), table_name="users")
    op.drop_table("user")

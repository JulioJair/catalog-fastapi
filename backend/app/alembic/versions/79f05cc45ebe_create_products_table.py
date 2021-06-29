"""create products table

Revision ID: 79f05cc45ebe
Revises: 3d4d62b34ef9
Create Date: 2021-06-28 13:13:13.406920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79f05cc45ebe'
down_revision = '3d4d62b34ef9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "analytics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("times_requested", sa.String(), nullable=True),
        sa.Column("product_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["product_id"], ["products.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_analytic_id"), "analytics", ["id"], unique=True)


def downgrade():
    pass

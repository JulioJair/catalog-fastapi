"""create users table

Revision ID: 3d4d62b34ef9
Revises: 
Create Date: 2021-06-28 13:12:58.446742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3d4d62b34ef9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("sku", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("price", sa.Float(), nullable=True),
        sa.Column("brand", sa.String(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_product_id"), "products", ["id"], unique=True)
    op.create_index(op.f("ix_product_name"), "products", ["name"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_product_id"), table_name="products")
    op.drop_index(op.f("ix_product_name"), table_name="products")
    op.drop_table("product")

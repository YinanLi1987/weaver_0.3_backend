"""add billed_amount to llm_usage_logs

Revision ID: 1ab84145b8c5
Revises: 259dba1902ab
Create Date: 2025-06-03 11:23:18.794095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ab84145b8c5'
down_revision: Union[str, None] = '259dba1902ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     op.add_column(
        "llm_usage_logs",
        sa.Column("billed_amount", sa.Numeric(10, 6), nullable=True)
    )


def downgrade() -> None:
    op.drop_column("llm_usage_logs", "billed_amount")

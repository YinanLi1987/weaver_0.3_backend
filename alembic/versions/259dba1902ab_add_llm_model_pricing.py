"""add llm model pricing

Revision ID: 259dba1902ab
Revises: 62541f49381c
Create Date: 2025-06-03 09:59:27.125354

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from decimal import Decimal

# revision identifiers, used by Alembic.
revision: str = '259dba1902ab'
down_revision: Union[str, None] = '62541f49381c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "llm_models",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("input_cost_per_1k", sa.Numeric(10, 6), nullable=False),
        sa.Column("output_cost_per_1k", sa.Numeric(10, 6), nullable=False),
       
    )
    llm_model_table = table(
        "llm_models",
        column("id", sa.String),
        column("name", sa.String),
        column("input_cost_per_1k", sa.Numeric(10, 6)),
        column("output_cost_per_1k", sa.Numeric(10, 6)),
    )

    op.bulk_insert(
        llm_model_table,
        [
            {
                "id": "gpt-4.1-nano",
                "name": "GPT-4.1 Nano",
                "input_cost_per_1k": Decimal("0.0001"),
                "output_cost_per_1k": Decimal("0.0004"),
            },
            {
                "id": "gpt-4",
                "name": "GPT-4",
                "input_cost_per_1k": Decimal("0.030"),
                "output_cost_per_1k": Decimal("0.060"),
            },
            {
                "id": "claude-3-7-sonnet",
                "name": "Claude Sonnet 3.7",
                "input_cost_per_1k": Decimal("0.003"),
                "output_cost_per_1k": Decimal("0.015"),
            },
            {
                "id": "mistral-small-latest",
                "name": "Mistral small",
                "input_cost_per_1k": Decimal("0.0000"),
                "output_cost_per_1k": Decimal("0.0000"),
            },
        ],
    )
    


def downgrade() -> None:
    op.drop_table("llm_models")

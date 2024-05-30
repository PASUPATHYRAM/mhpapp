"""adding_table_contact

Revision ID: 3bc8f90fc05b
Revises: c0de76bf3f4b
Create Date: 2024-05-13 10:31:33.348945

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bc8f90fc05b'
down_revision: Union[str, None] = 'c0de76bf3f4b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:


    op.create_table(
        'park_contact',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('address_fk', sa.String(), sa.ForeignKey('park_details.address_line_1')),
        sa.Column('website', sa.String(), nullable=True),
        sa.Column('contact_person', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('phone', sa.Integer(), nullable=True)
    )


def downgrade() -> None:
    pass

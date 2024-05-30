"""changing phone to string

Revision ID: 5cc2bd5624f7
Revises: 3bc8f90fc05b
Create Date: 2024-05-13 11:27:03.404810

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5cc2bd5624f7'
down_revision: Union[str, None] = '3bc8f90fc05b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('park_contact','phone',existing_type=sa.Integer(),
                    type_=sa.String(),existing_nullable=True)



def downgrade() -> None:
    pass

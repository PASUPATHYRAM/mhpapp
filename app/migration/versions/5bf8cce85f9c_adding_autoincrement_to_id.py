"""adding autoincrement to id

Revision ID: 5bf8cce85f9c
Revises: 5cc2bd5624f7
Create Date: 2024-05-13 11:35:30.314553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bf8cce85f9c'
down_revision: Union[str, None] = '5cc2bd5624f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('park_contact','id',
                    existing_type=sa.Integer(),
                    autoincrement=True)



def downgrade() -> None:
    pass

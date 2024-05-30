"""Change park_name to primary key

Revision ID: bf7c415f8547
Revises: 
Create Date: 2024-05-08 15:41:25.853567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf7c415f8547'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('park_details',schema=None) as ba_op:
        ba_op.drop_constraint('park_details_pkey',type_='primary')
        ba_op.alter_column('park_name',existing_type=sa.String(),nullable=False)
        ba_op.create_primary_key(None,['park_name'])


def downgrade() -> None:
    pass

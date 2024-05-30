"""pk to address

Revision ID: c0de76bf3f4b
Revises: bf7c415f8547
Create Date: 2024-05-11 12:29:16.901754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0de76bf3f4b'
down_revision: Union[str, None] = 'bf7c415f8547'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('park_details',schema=None) as ba_op:
        ba_op.drop_constraint('park_details_pkey',type_='primary')
        ba_op.create_primary_key(None,['address_line_1'])

    print("creating table")

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

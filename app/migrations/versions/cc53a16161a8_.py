"""empty message

Revision ID: cc53a16161a8
Revises: 8638a0651189
Create Date: 2024-03-11 22:43:57.775403

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc53a16161a8'
down_revision: Union[str, None] = '8638a0651189'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tickets', sa.Column('number_ticket', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tickets', 'number_ticket')
    # ### end Alembic commands ###
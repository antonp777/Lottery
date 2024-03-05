"""CreateTable

Revision ID: 504f07910e50
Revises: 
Create Date: 2024-03-05 01:55:45.313386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '504f07910e50'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('lotterys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('number_tickets', sa.Integer(), nullable=False),
    sa.Column('price_ticket', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'NONACTIVE', name='lotterystatus'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usersAdmin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions_coming',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('sum', sa.Integer(), nullable=False),
    sa.Column('comment', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('OK', 'NOTOK', 'WAIT', name='transcomingstatus'), nullable=False),
    sa.Column('prichinaOtkaza', sa.String(), nullable=True),
    sa.Column('message_id', sa.Integer(), nullable=True),
    sa.Column('id_trans_expence_info', sa.Integer(), nullable=True),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_card', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_card'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('transactions_expense',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('sum', sa.Integer(), nullable=False),
    sa.Column('count_tickets', sa.Integer(), nullable=False),
    sa.Column('status', sa.Enum('OK', 'WAIT', name='transexpensestatus'), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_lottery', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_lottery'], ['lotterys.id'], ),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('isFinish', sa.Boolean(), nullable=False),
    sa.Column('status', sa.Enum('OK', 'WAIT', name='ticketstatus'), nullable=False),
    sa.Column('id_user', sa.Integer(), nullable=False),
    sa.Column('id_lottery', sa.Integer(), nullable=False),
    sa.Column('id_trans_expense', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_lottery'], ['lotterys.id'], ),
    sa.ForeignKeyConstraint(['id_trans_expense'], ['transactions_expense.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['id_user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tickets')
    op.drop_table('transactions_expense')
    op.drop_table('transactions_coming')
    op.drop_table('usersAdmin')
    op.drop_table('users')
    op.drop_table('lotterys')
    op.drop_table('cards')
    # ### end Alembic commands ###

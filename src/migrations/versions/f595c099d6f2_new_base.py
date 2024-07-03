"""new_base

Revision ID: f595c099d6f2
Revises: 
Create Date: 2024-05-27 15:37:48.153548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f595c099d6f2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Documents',
    sa.Column('ID_doc', sa.Integer(), nullable=False),
    sa.Column('psth', sa.String(), nullable=False),
    sa.Column('date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('ID_doc')
    )
    op.create_table('Documents_text',
    sa.Column('ID', sa.Integer(), nullable=False),
    sa.Column('ID_doc', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['ID_doc'], ['Documents.ID_doc'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('ID')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Documents_text')
    op.drop_table('Documents')
    # ### end Alembic commands ###
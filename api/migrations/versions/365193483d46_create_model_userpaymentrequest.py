"""create model UserPaymentRequest

Revision ID: 365193483d46
Revises: e92eba811580
Create Date: 2023-10-27 11:13:04.975930

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '365193483d46'
down_revision = 'e92eba811580'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('userpayment_requests',
    sa.Column('idx', sa.BigInteger(), nullable=False),
    sa.Column('user', sa.BigInteger(), nullable=True),
    sa.Column('course', sa.BigInteger(), nullable=True),
    sa.Column('is_success', sa.Boolean(), nullable=True),
    sa.Column('receipt', sa.String(length=1024), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course'], ['courses.idx'], name='fk_userpayment_requests_courses_idx_course'),
    sa.ForeignKeyConstraint(['user'], ['users.idx'], name='fk_userpayment_requests_users_idx_user'),
    sa.PrimaryKeyConstraint('idx')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('userpayment_requests')
    # ### end Alembic commands ###
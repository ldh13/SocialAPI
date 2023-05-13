"""add user table

Revision ID: d22b8567fbe9
Revises: 90e6c6be6b1d
Create Date: 2023-05-13 15:29:25.231442

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd22b8567fbe9'
down_revision = '90e6c6be6b1d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable= False),
        sa.Column('email', sa.String(), nullable= False),
        sa.Column('password', sa.String(), nullable= False),
        sa.Column('created_at', sa.TIMESTAMP(timezone= True), server_default= sa.text('NOW()'), nullable= False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')

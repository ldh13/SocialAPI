"""add content column to posts table

Revision ID: 90e6c6be6b1d
Revises: 9a8e4722ed59
Create Date: 2023-05-13 15:21:44.040667

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90e6c6be6b1d'
down_revision = '9a8e4722ed59'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable= False)
        )


def downgrade():
    op.drop_column('posts', 'content')

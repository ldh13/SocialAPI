"""add last few columns to posts table

Revision ID: e5d3d2a869ec
Revises: e7a06548fe91
Create Date: 2023-05-13 15:42:16.825248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5d3d2a869ec'
down_revision = 'e7a06548fe91'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean, nullable= False, server_default='TRUE')

    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable= False, server_default= sa.text('NOW()'))
    )


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

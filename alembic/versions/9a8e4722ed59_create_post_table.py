"""create post table

Revision ID: 9a8e4722ed59
Revises: 
Create Date: 2023-05-13 15:09:44.133331

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a8e4722ed59'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), nullable= False, primary_key= True),
        sa.Column('title', sa.String(), nullable= False)
        )


def downgrade():
    op.drop_table('posts')
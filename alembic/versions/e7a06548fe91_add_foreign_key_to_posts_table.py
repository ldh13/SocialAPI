"""add foreign key to posts table

Revision ID: e7a06548fe91
Revises: d22b8567fbe9
Create Date: 2023-05-13 15:37:56.491165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7a06548fe91'
down_revision = 'd22b8567fbe9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('user_id', sa.Integer(), nullable= False)
        )
    op.create_foreign_key(
        'posts_users_fk',
        source_table='posts',
        referent_table='users',
        local_cols= ['user_id'],
        remote_cols= ['id'],
        ondelete='CASCADE'
        )


def downgrade():
    op.drop_constraint(
        'post_users_fk',
        table_name='posts'
        )
    op.drop_column('posts', 'user_id')

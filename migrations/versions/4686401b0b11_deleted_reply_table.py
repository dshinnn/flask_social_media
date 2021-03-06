"""Deleted reply table

Revision ID: 4686401b0b11
Revises: 1e88296eb198
Create Date: 2022-01-22 19:49:24.285489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4686401b0b11'
down_revision = '1e88296eb198'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reply')
    op.add_column('comment', sa.Column('parent_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'comment', 'comment', ['parent_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'comment', type_='foreignkey')
    op.drop_column('comment', 'parent_id')
    op.create_table('reply',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('reply_section', sa.VARCHAR(length=256), autoincrement=False, nullable=False),
    sa.Column('post_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('comment_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.id'], name='reply_comment_id_fkey'),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], name='reply_post_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='reply_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='reply_pkey')
    )
    # ### end Alembic commands ###

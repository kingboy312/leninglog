"""empty message

Revision ID: 3181495c0703
Revises: 
Create Date: 2020-07-03 18:32:45.850944

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3181495c0703'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    op.create_table('topic',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('topic_s', sa.String(length=100), nullable=True),
                    sa.Column('enty_id', sa.Integer(), nullable=True),
                    sa.Column('user_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('empty',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('empty', sa.String(length=1000), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('topic_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['topic_id'], ['topic.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_empty_add_time'), 'empty', ['add_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('topic')
    op.drop_index(op.f('ix_empty_add_time'), table_name='empty')
    op.drop_table('empty')
    # ### end Alembic commands ###
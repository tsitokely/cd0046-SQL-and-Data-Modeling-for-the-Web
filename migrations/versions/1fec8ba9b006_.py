"""empty message

Revision ID: 1fec8ba9b006
Revises: 
Create Date: 2022-08-20 14:17:05.990754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fec8ba9b006'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('City',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('city', sa.String(length=120), nullable=True),
    sa.Column('state', sa.String(length=120), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('Artist', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Artist', 'City', ['city_id'], ['id'])
    op.drop_column('Artist', 'state')
    op.drop_column('Artist', 'city')
    op.add_column('Venue', sa.Column('city_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'Venue', 'City', ['city_id'], ['id'])
    op.drop_column('Venue', 'state')
    op.drop_column('Venue', 'city')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Venue', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'city_id')
    op.add_column('Artist', sa.Column('city', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('state', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Artist', type_='foreignkey')
    op.drop_column('Artist', 'city_id')
    op.drop_table('City')
    # ### end Alembic commands ###

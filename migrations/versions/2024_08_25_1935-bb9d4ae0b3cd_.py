"""empty message

Revision ID: bb9d4ae0b3cd
Revises: a2b246556fde
Create Date: 2024-08-25 19:35:44.951016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bb9d4ae0b3cd'
down_revision: Union[str, None] = 'a2b246556fde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cities', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.SmallInteger(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('cities_id_seq'::regclass)"))
    op.alter_column('cities_metro_stations', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.SmallInteger(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('metro_stations', 'id',
               existing_type=sa.INTEGER(),
               type_=sa.SmallInteger(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('metro_stations_id_seq'::regclass)"))
    op.drop_index('ix_parsing_results_floor_flat_area', table_name='parsing_results')
    op.create_index(op.f('ix_parsing_results_direct_link'), 'parsing_results', ['direct_link'], unique=False)
    op.drop_column('parsing_results', 'listed_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parsing_results', sa.Column('listed_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_parsing_results_direct_link'), table_name='parsing_results')
    op.create_index('ix_parsing_results_floor_flat_area', 'parsing_results', ['floor', 'flat_area'], unique=False)
    op.alter_column('metro_stations', 'id',
               existing_type=sa.SmallInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('metro_stations_id_seq'::regclass)"))
    op.alter_column('cities_metro_stations', 'id',
               existing_type=sa.SmallInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True)
    op.alter_column('cities', 'id',
               existing_type=sa.SmallInteger(),
               type_=sa.INTEGER(),
               existing_nullable=False,
               autoincrement=True,
               existing_server_default=sa.text("nextval('cities_id_seq'::regclass)"))
    # ### end Alembic commands ###

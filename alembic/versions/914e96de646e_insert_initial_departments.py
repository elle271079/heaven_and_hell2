"""Insert initial departments

Revision ID: 914e96de646e
Revises: 8331418dd999
Create Date: 2022-04-18 21:01:17.404178

"""
from alembic import op
from sqlalchemy.orm import sessionmaker
from db.model import Department

revision = '914e96de646e'
down_revision = '8331418dd999'
branch_labels = None
depends_on = None

Session = sessionmaker(bind=op.get_bind())


def upgrade():
    session = Session()
    session.add_all([
        Department(name="Learning", budget=500000, address="Ashford Close 12 Birmingham B24 0JD"),
        Department(name="Admin", budget=20000, address="Ashford Close 12 Birmingham B24 0JD"),
        Department(name="IT", budget=10000, address="Lichfield 10 Birmingham B18 99D")
    ])
    session.commit()


def downgrade():
    pass
    # engine = op.get_bind()
    # engine.execute("TRUNCATE department")


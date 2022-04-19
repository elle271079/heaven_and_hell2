"""Initial

Revision ID: 8331418dd999
Revises: 
Create Date: 2022-04-18 20:56:58.387696

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8331418dd999'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('department',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('budget', sa.Numeric(precision=32), nullable=True),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staff',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('enrollment_date', sa.DateTime(), nullable=True),
    sa.Column('pesel', sa.Numeric(precision=11), nullable=False),
    sa.Column('phone', sa.Numeric(precision=16), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('pesel', sa.String(length=11), nullable=False),
    sa.Column('phone', sa.String(length=32), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pesel')
    )
    op.create_table('administrator',
    sa.Column('staff_id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.Column('enrollment_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['department.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.PrimaryKeyConstraint('staff_id', 'department_id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('credits', sa.Numeric(precision=32), nullable=True),
    sa.Column('departament_id', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('price', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['departament_id'], ['department.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_instructor',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=False),
    sa.Column('enrollment_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'staff_id')
    )
    op.create_table('online_courses',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('onsite_courses',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=False),
    sa.Column('days', sa.Numeric(precision=64), nullable=True),
    sa.Column('time', sa.Numeric(precision=64), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('course_id')
    )
    op.create_table('student_grades',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )


def downgrade():
    op.drop_table('student_grades')
    op.drop_table('onsite_courses')
    op.drop_table('online_courses')
    op.drop_table('course_instructor')
    op.drop_table('courses')
    op.drop_table('administrator')
    op.drop_table('students')
    op.drop_table('staff')
    op.drop_table('department')

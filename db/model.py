from faker import Faker
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from pesel import Pesel

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    pesel = Column(String(11), unique=True, nullable=False)
    phone = Column(String(32), nullable=False)
    address = Column(String(64))

    # relacja wielu do wielu
    courses = relationship("Course", back_populates="students", secondary="student_grades")

    def __repr__(self):
        return f"Student({self.id}, {self.first_name}, {self.last_name}, {self.phone})"

    @staticmethod
    def create_fake_student():
        fake = Faker()
        return Student(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            pesel=Pesel.generate(),
            phone=fake.phone_number(),
            address=fake.address()
            )


def create_fake_students(session, count=50):
    student_generated = 0
    while student_generated < count:
        try:
            session.add(Student.create_fake_student())
            session.commit()
        except IntegrityError:
            session.rollback()
            continue
        student_generated += 1


class Department(Base):
    __tablename__ = "department"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    budget = Column(Numeric(32))
    address = Column(String(64))

    dept_id1 = relationship("Course", back_populates="dept")

    # relacja wielu do wielu
    staff = relationship("Staff", back_populates="department", secondary="administrator")

    def __repr__(self):
        return f"Department({self.id}, {self.name}, {self.address})"


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    credits = Column(Numeric(32))
    departament_id = Column(Integer, ForeignKey("department.id"), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    price = Column(Numeric)

    dept = relationship(Department, back_populates="dept_id1")
    course_id1 = relationship("OnlineCourse", back_populates="course_online")
    course_id2 = relationship("OnsiteCourse", back_populates="course_onsite")

    # relacja wielu do wielu
    staff = relationship("Staff", back_populates="courses", secondary="course_instructor")
    students = relationship(Student, back_populates="courses", secondary="student_grades")

    def __repr__(self):
        return f"Course({self.id}, {self.title}, {self.start_date}, {self.end_date}, {self.price})"


class OnlineCourse(Base):
    __tablename__ = "online_courses"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    url = Column(String(100), nullable=False)

    course_online = relationship(Course, back_populates="course_id1")

    def __repr__(self):
        return f"Online Course({self.course_id}, {self.url})"


class OnsiteCourse(Base):
    __tablename__ = "onsite_courses"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    address = Column(String(64), nullable=False)
    days = Column(Numeric(64))
    time = Column(Numeric(64))

    course_onsite = relationship(Course, back_populates="course_id2")

    def __repr__(self):
        return f"Onsite Course({self.course_id}, {self.address}, {self.days}, {self.time})"


class StudentGrade(Base):
    __tablename__ = "student_grades"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    grade = Column(String(100))


class Staff(Base):
    __tablename__ = "staff"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    enrollment_date = Column(DateTime)
    pesel = Column(Numeric(11), nullable=False)
    phone = Column(Numeric(16), nullable=False)
    address = Column(String(64))

    # relacja wielu do wielu
    courses = relationship(Course, back_populates="staff", secondary="course_instructor")
    department = relationship(Department, back_populates="staff", secondary="administrator")

    def __repr__(self):
        return f"Staff({self.id}, {self.first_name}, {self.last_name}, {self.phone})"


class CourseInstructor(Base):
    __tablename__ = "course_instructor"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    enrollment_date = Column(DateTime)


class Administrator(Base):
    __tablename__ = "administrator"

    staff_id = Column(Integer, ForeignKey("staff.id"), primary_key=True)
    department_id = Column(Integer, ForeignKey("department.id"), primary_key=True)
    enrollment_date = Column(DateTime)

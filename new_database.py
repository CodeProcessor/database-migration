from sqlalchemy import DATETIME, NVARCHAR, Column, Float, Integer

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Student(Base):
    """Student table to store student information"""

    __tablename__ = "students"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    student_id = Column(NVARCHAR(20), unique=True, index=True)
    first_name = Column(NVARCHAR(50), nullable=False)
    last_name = Column(NVARCHAR(50), nullable=False)
    email = Column(NVARCHAR(100), unique=True)
    date_of_birth = Column(DATETIME, nullable=False)
    grade_level = Column(Integer(), nullable=False)
    # gpa = Column(Float(), default=0.0)
    marks = Column(Float(), default=0.0)

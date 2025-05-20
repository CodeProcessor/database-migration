from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger

from db_utils import get_session
from old_database import Base, Student


def create_old_database(conn_string):
    with get_session(conn_string) as session:
        # Create all tables
        Base.metadata.create_all(session.get_bind())

        # Add sample records
        sample_records = [
            Student(
                student_id="STU001",
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                date_of_birth=datetime(1990, 1, 15),
                grade_level=10,
                gpa=2.7,
            ),
            Student(
                student_id="STU002",
                first_name="Jane",
                last_name="Smith",
                email="jane.smith@example.com",
                date_of_birth=datetime(1992, 5, 20),
                grade_level=11,
                gpa=3.5,
            ),
        ]

        session.add_all(sample_records)
        session.commit()

        logger.info("Database created and sample records added successfully!")


if __name__ == "__main__":
    create_old_database("sqlite:///old_database.db")

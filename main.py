from datetime import datetime
from zoneinfo import ZoneInfo

from loguru import logger

from db_utils import get_session
from old_database import Base, SampleTable

# Create database and add sample records
conn_string = "sqlite:///old_database.db"


def main():
    with get_session(conn_string) as session:
        # Create all tables
        Base.metadata.create_all(session.get_bind())

        # Add sample records
        sample_records = [
            SampleTable(
                request_id="REQ001",
                extracted_text="Sample text 1",
                external_id="EXT001",
                job_start_time=datetime.now(ZoneInfo("UTC")),
                job_end_time=datetime.now(ZoneInfo("UTC")),
                total_job_time_seconds=10.5,
            ),
            SampleTable(
                request_id="REQ002",
                extracted_text="Sample text 2",
                external_id="EXT002",
                job_start_time=datetime.now(ZoneInfo("UTC")),
                job_end_time=datetime.now(ZoneInfo("UTC")),
                total_job_time_seconds=15.2,
            ),
        ]

        session.add_all(sample_records)
        session.commit()

        logger.info("Database created and sample records added successfully!")


if __name__ == "__main__":
    main()

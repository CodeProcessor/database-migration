from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import DATETIME, NVARCHAR, Column, Float, Integer, UnicodeText

# from sqlalchemy.dialects.mssql import DATETIMEOFFSET
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SampleTable(Base):
    """TitleExtractionJobs table to keep the job details"""

    __tablename__ = "sample_table"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    request_id = Column(NVARCHAR(40), unique=True, index=True)
    extracted_text = Column(UnicodeText(), nullable=True)
    external_id = Column(NVARCHAR(256), nullable=True)
    job_start_time = Column(DATETIME, default=datetime.now(ZoneInfo("UTC")))
    job_end_time = Column(DATETIME)
    total_job_time_seconds = Column(Float(), default=0.0)

import asyncio
import os

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.future import select

from alembic.command import upgrade, stamp
from alembic.config import Config


async def add_data_to_database(engine: AsyncEngine) -> None:
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        try:
            from datetime import datetime
            from zoneinfo import ZoneInfo

            from new_database import Student

            sample_records = [
                {
                    "student_id": "STU003", 
                    "first_name": "Michael",
                    "last_name": "Johnson",
                    "email": "michael.johnson@example.com",
                    "date_of_birth": datetime(1991, 8, 12),
                    "grade_level": 10,
                    "marks": 92.5,
                },
                {
                    "student_id": "STU004",
                    "first_name": "Emily",
                    "last_name": "Brown",
                    "email": "emily.brown@example.com", 
                    "date_of_birth": datetime(1993, 3, 25),
                    "grade_level": 11,
                    "marks": 89.5,
                },
            ]

            for record in sample_records:
                # Check if record exists
                existing_record = (
                    await session.execute(
                        select(Student).filter_by(student_id=record["student_id"])
                    )
                ).scalar()

                if not existing_record:
                    new_record = Student(
                        student_id=record["student_id"],
                        first_name=record["first_name"],
                        last_name=record["last_name"],
                        email=record["email"],
                        date_of_birth=record["date_of_birth"],
                        grade_level=record["grade_level"],
                        marks=record["marks"],
                    )
                    session.add(new_record)
                    logger.info(f"Added record with student_id: {record['student_id']}")
                else:
                    logger.info(
                        f"Record with student_id: {record['student_id']} already exists"
                    )
            await session.commit()
        except Exception as error:
            logger.error(f"Error adding data to database: {error}")
            await session.rollback()
            raise error


def run_upgrade(conn, config) -> None:
    config.attributes["connection"] = conn
    upgrade(config, "head")


async def run_db_migrations(connection_string: str, debug_mode: bool) -> None:
    """Run db migrations"""
    logger.info("Starting run db migrations")
    # retrieves the directory that *this* file is in
    migrations_dir = os.path.dirname(os.path.realpath(__file__))
    # this assumes the alembic.ini is also contained in this same directory
    config_file = os.path.join(migrations_dir, "alembic.ini")
    config = Config(config_file)

    # Override the connection string from alembic.ini
    config.set_main_option("sqlalchemy.url", connection_string)

    # Create alembic_version table and stamp it to head if it doesn't exist
    try:
        engine = create_async_engine(connection_string, echo=debug_mode)
        async with engine.begin() as conn:
            # Check if alembic_version table exists
            has_table = await conn.run_sync(
                lambda sync_conn: sync_conn.dialect.has_table(sync_conn, "alembic_version")
            )
            # Check if other tables exist
            has_other_tables = await conn.run_sync(
                lambda sync_conn: bool(sync_conn.dialect.get_table_names(sync_conn))
            )

            # If alembic_version table doesn't exist and other tables exist, create and stamp to head
            if not has_table and has_other_tables:
                logger.info("Alembic version table not found - creating and stamping to head")
                # Create alembic_version table and stamp it to head
                await conn.run_sync(lambda sync_conn: stamp(config, "3b5fa40dd45d"))
    except Exception as e:
        logger.error(f"Error checking/creating alembic version: {e}")
        raise

    engine = create_async_engine(connection_string, echo=debug_mode)
    async with engine.begin() as conn:
        await conn.run_sync(run_upgrade, config)

    await add_data_to_database(engine)


if __name__ == "__main__":
    # Using aiosqlite driver for async SQLite support
    asyncio.run(run_db_migrations("sqlite+aiosqlite:///old_database.db", True))

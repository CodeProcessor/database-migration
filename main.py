import asyncio

from loguru import logger

from alembic_main import run_db_migrations
from sqlite_main import create_old_database


def main():
    # Remove old database file if it exists
    import os

    if os.path.exists("old_database.db"):
        os.remove("old_database.db")
        logger.info("Old database file removed")

    # create old database without alembic
    create_old_database("sqlite:///old_database.db")

    # add alembic migrations
    asyncio.run(run_db_migrations("sqlite+aiosqlite:///old_database.db", True))


if __name__ == "__main__":
    main()

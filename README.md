# Database Migration with Alembic
 
This project demonstrates how to export an existing database schema to Alembic migrations and manage database changes.

## Overview
The project shows how to:
- Capture an existing database schema using SQLAlchemy models
- Initialize Alembic for migration management
- Generate initial migration from existing database
- Make and track schema changes with Alembic

## Prerequisites
- Python 3.12+
- SQLAlchemy 2.0+
- Alembic
- Database driver for your database (e.g., pyodbc for MSSQL)

## Setup

1. Install dependencies:

If you haven’t already, install Alembic in your environment:

```bash
uv add alembic
uv add aiosqlite

or 

uv sync
```

2. Initialize Alembic

Run the following command in your project root to set up Alembic’s directory and configuration files:
```bash
alembic init alembic
```

3. Configure Alembic

+ Set your database URL in alembic.ini.
+ In alembic/env.py, set target_metadata to your models’ metadata.

4. Generate Initial Migration

If you haven’t already, generate a migration that reflects your models:

```bash
alembic revision --autogenerate -m "Initial migration"
```

### For existing databases

If the generated migration is empty (no operations), that means the database is uptodate. 
You can delete this file because it is not usable. 

#### _Important_
But if you want to have the initial database creation script, point the database url to a new location and run the above, then it will create the initial creation scripts. Which can be used to 
create fresh database. 

5. Stamp the database

Tell Alembic to consider your current database as up-to-date with the latest migration, without applying any changes:
```
alembic stamp head
```


This creates the alembic_version table and marks your database as current.


To stamp your database with a specific Alembic revision (not just "head"), use the following command:

```
alembic stamp <revision_id>
```
This is useful when you want Alembic to consider your database as being at a specific migration state, even if you did not actually run the migration scripts for that revision (for example, if you manually applied schema changes or are aligning environments)

6. Future Migrations

Now, whenever you change your models, you can use:

```
alembic revision --autogenerate -m "Describe your change"
alembic upgrade head
```
This will generate and apply new migrations as your schema evolves.


## About this example

This example demonstrates how to handle database migrations with Alembic in two scenarios:

1. Creating a new database from scratch using Alembic migrations
2. Adding Alembic support to an existing database

The code includes:

- A SQLAlchemy model (`Student`) defining the database schema
- Scripts to create a database both with and without Alembic:
  - `sqlite_main.py` - Creates database directly using SQLAlchemy
  - `alembic_main.py` - Handles Alembic migrations and versioning
- Sample data population
- Proper handling of the alembic_version table

Key points demonstrated:

- How to stamp an existing database with Alembic version
- Checking for existing alembic_version table
- Adding sample data safely with duplicate checks
- Async database operations with SQLite
- Proper error handling and logging

The example uses SQLite for simplicity but the concepts apply to any SQL database supported by SQLAlchemy.


## Code Walkthrough

The `main.py` file demonstrates the migration process in two key steps:

1. Initial Database Creation:
   - Creates database using plain SQLAlchemy via `create_old_database()`
   - Sets up tables and initial data without any Alembic versioning
   - Uses `sqlite_main.py` to handle the schema creation

2. Adding Alembic Support:
   - Calls `run_db_migrations()` to add Alembic versioning
   - Checks if alembic_version table exists
   - Stamps the database with revision "3b5fa40dd45d" to mark current state
   - Enables future schema changes to be tracked via migrations

This two-step process shows how to properly transition an existing database to use Alembic for version control.




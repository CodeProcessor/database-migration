# database-migration

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


Process
uv add alembic
alembic init alembic

"""
database.py — Database configuration for Life Dashboard.

Sets up:
  - SQLite database engine
  - Session factory (SessionLocal)
  - Declarative base for ORM models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file will be created in the project root
DATABASE_URL = "sqlite:///./life_dashboard.db"

# Create the SQLAlchemy engine
# 'check_same_thread=False' is needed for SQLite with FastAPI (multi-threaded)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our ORM models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Yields a session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

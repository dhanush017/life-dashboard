"""
database.py — Database configuration for Life Dashboard.

Sets up:
  - SQLite database engine (development)
  - PostgreSQL database engine (production)
  - Session factory (SessionLocal)
  - Declarative base for ORM models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Get DATABASE_URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./life_dashboard.db")

# For PostgreSQL, disable SSL verification in production
connect_args = {}
if "postgresql" in DATABASE_URL:
    # PostgreSQL connection
    connect_args = {"sslmode": "require"}
else:
    # SQLite connection
    connect_args = {"check_same_thread": False}

# Create the SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,  # Test connection before using (helps with stale connections)
    pool_size=5,
    max_overflow=10,
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

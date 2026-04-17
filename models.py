"""
models.py — SQLAlchemy ORM models for Life Dashboard.

Defines the User and LifeData tables for multi-user habit tracking.
"""

from sqlalchemy import Column, Integer, Float, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """
    Represents a registered user of the Life Dashboard.

    Fields:
        id           — Auto-incrementing primary key
        username     — Unique username for login
        email        — User's email address
        hashed_password — Bcrypt hash of user's password
        created_at   — Account creation timestamp
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)

    # Relationship to life data entries
    life_entries = relationship("LifeData", back_populates="user")


class LifeData(Base):
    """
    Represents one day's worth of tracked life data for a specific user.

    Fields:
        id           — Auto-incrementing primary key
        user_id      — Foreign key to the user who owns this entry
        study_hours  — Hours spent studying (e.g. 3.5)
        sleep_hours  — Hours of sleep (e.g. 7.0)
        screen_time  — Hours of screen usage (e.g. 5.0)
        mood         — Self-reported mood from 1 (worst) to 10 (best)
        date         — The date this entry corresponds to (YYYY-MM-DD)
    """

    __tablename__ = "life_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    study_hours = Column(Float, nullable=False)
    sleep_hours = Column(Float, nullable=False)
    screen_time = Column(Float, nullable=False)
    mood = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)

    # Relationship to user
    user = relationship("User", back_populates="life_entries")

    # Ensure each user can only have one entry per date
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='unique_user_date'),
    )

"""
schemas.py — Pydantic schemas for request/response validation.

These schemas ensure that data coming in and going out of
the API is properly typed and validated.
"""

from pydantic import BaseModel, Field, EmailStr
from datetime import date as DateType
from typing import Optional


class LifeDataCreate(BaseModel):
    """Schema for creating a new daily entry via POST /add-data."""

    study_hours: float = Field(..., ge=0, le=24, description="Hours spent studying")
    sleep_hours: float = Field(..., ge=0, le=24, description="Hours of sleep")
    screen_time: float = Field(..., ge=0, le=24, description="Hours of screen usage")
    mood: int = Field(..., ge=1, le=10, description="Mood rating from 1 to 10")
    date: DateType = Field(..., description="Date of the entry (YYYY-MM-DD)")


class LifeDataResponse(BaseModel):
    """Schema for returning a stored entry via GET /get-data."""

    id: int
    study_hours: float
    sleep_hours: float
    screen_time: float
    mood: int
    date: DateType

    class Config:
        from_attributes = True  # Allows reading data from ORM model instances

class UserCreate(BaseModel):
    """Schema for creating a new user account."""

    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, max_length=128, description="User's password (6-128 characters)")


class UserLogin(BaseModel):
    """Schema for user login."""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    """Schema for returning user information."""

    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication tokens."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload data."""

    username: Optional[str] = None


class ChatRequest(BaseModel):
    message: str = Field(..., description="User's query to the AI")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI's response")

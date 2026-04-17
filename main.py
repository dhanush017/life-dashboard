"""
main.py — FastAPI application for Life Dashboard.

Endpoints:
  POST /add-data    — Save a daily entry
  GET  /get-data    — Retrieve all entries
  GET  /insights    — Compute stats + AI insights
  GET  /export      — Download data as CSV
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Any
from datetime import timedelta
import traceback
import io
import csv
import pandas as pd
import os

from database import engine, get_db, Base
from models import User, LifeData
from schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    LifeDataCreate, LifeDataResponse
)
from analysis import compute_stats
from ai_insights import generate_insights
from auth import (
    authenticate_user, create_access_token, get_current_active_user,
    get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
)
from logging_config import get_logger
from rate_limiting import get_limiter_dependency, RATE_LIMITS
from dotenv import load_dotenv

load_dotenv()

# Initialize logger
logger = get_logger("lifedashboard.main")

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Life Dashboard",
    description="A habit tracking system that doesn't just store data — it explains it.",
    version="1.0.0",
)

# ===== CORS CONFIGURATION =====
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
is_production = os.getenv("ENVIRONMENT") == "production"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


# ===== GLOBAL EXCEPTION HANDLERS =====

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Catch ALL unhandled exceptions, log them, and return a proper JSON response.
    This prevents "Internal Server Error" crashes and provides useful error info.
    """
    error_id = id(exc)  # Unique error identifier for tracking
    
    # Log the full stack trace for debugging
    logger.error(
        f"Unhandled exception (ID: {error_id}): {type(exc).__name__}",
        exc_info=True,
        extra={
            "path": request.url.path,
            "method": request.method,
            "client": request.client.host if request.client else "unknown",
        }
    )
    
    # Return a safe error response to the client
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred.",
            "error_id": error_id,
            "message": "Please contact support with the error ID if the problem persists.",
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle database errors gracefully."""
    error_id = id(exc)
    
    logger.error(
        f"Database error (ID: {error_id}): {str(exc)}",
        exc_info=True,
        extra={"path": request.url.path, "method": request.method}
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database error occurred.",
            "error_id": error_id,
            "message": "The database operation failed. Please try again.",
        }
    )


# ===== CUSTOM ERROR HANDLER FOR VALIDATION ERRORS =====
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    """Handle validation errors with user-friendly messages."""
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {exc}",
        extra={"path": request.url.path}
    )
    
    errors = []
    for error in exc.errors():
        field = ".".join(str(x) for x in error["loc"][1:])
        msg = error["msg"]
        errors.append(f"{field}: {msg}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "; ".join(errors)
        }
    )


# ===== AUTHENTICATION ENDPOINTS =====

@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    logger.info(f"Registration attempt for username: {user.username}")
    
    try:
        # Check if username already exists
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            logger.warning(f"Registration failed: username '{user.username}' already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Check if email already exists
        db_user = db.query(User).filter(User.email == user.email).first()
        if db_user:
            logger.warning(f"Registration failed: email '{user.email}' already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user.password)
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered successfully: {user.username} (ID: {db_user.id})")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error for {user.username}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Registration failed"
        )


@app.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authenticate user and return JWT access token."""
    logger.info(f"Login attempt for username: {form_data.username}")
    
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in successfully: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}


# ----- Serve the frontend -----

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the single-page dashboard."""
    return FileResponse("index.html")


# ----- API Endpoints -----

@app.post("/add-data", response_model=LifeDataResponse)
def add_data(
    entry: LifeDataCreate,
    current_user: User = Depends(get_current_active_user),
    _rate_limit: bool = Depends(get_limiter_dependency("add_data")),
    db: Session = Depends(get_db)
):
    """
    Save a new daily entry to the database for the current user.

    Expects JSON body with: study_hours, sleep_hours, screen_time, mood, date
    Returns the created entry with its assigned ID.
    """
    logger.debug(f"Adding data entry for user {current_user.username} on {entry.date}")

    # Check if an entry for this date already exists for this user
    existing = db.query(LifeData).filter(
        LifeData.user_id == current_user.id,
        LifeData.date == entry.date
    ).first()
    if existing:
        logger.warning(f"Duplicate entry attempt for user {current_user.username} on {entry.date}")
        raise HTTPException(
            status_code=400,
            detail=f"An entry for {entry.date} already exists. Each date must be unique."
        )

    # Create and save the new entry
    db_entry = LifeData(
        user_id=current_user.id,
        study_hours=entry.study_hours,
        sleep_hours=entry.sleep_hours,
        screen_time=entry.screen_time,
        mood=entry.mood,
        date=entry.date,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    logger.info(f"Data entry saved for user {current_user.username} on {entry.date} (ID: {db_entry.id})")

    return db_entry


@app.get("/get-data", response_model=list[LifeDataResponse])
def get_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all stored entries for the current user, ordered by date (most recent first).
    """
    logger.debug(f"Retrieving data for user {current_user.username}")
    
    entries = db.query(LifeData).filter(
        LifeData.user_id == current_user.id
    ).order_by(LifeData.date.desc()).all()
    logger.debug(f"Retrieved {len(entries)} entries for user {current_user.username}")
    return entries


@app.get("/insights")
async def get_insights(
    current_user: User = Depends(get_current_active_user),
    _rate_limit: bool = Depends(get_limiter_dependency("get_insights")),
    db: Session = Depends(get_db)
) -> dict[str, Any]:
    """
    The core feature of Life Dashboard.

    1. Pulls all data from the database for the current user
    2. Computes statistics (averages, correlations, trends)
    3. Sends stats to Claude for human-readable insights
    4. Returns both raw stats and AI insights as JSON

    Requires at least 3 entries to generate meaningful insights.
    """

    # Fetch all entries for the current user
    entries = db.query(LifeData).filter(
        LifeData.user_id == current_user.id
    ).order_by(LifeData.date.asc()).all()

    # Edge case: not enough data
    if len(entries) < 3:
        return {
            "status": "insufficient_data",
            "message": f"You have {len(entries)} entries. Add at least 3 entries to unlock insights.",
            "stats": None,
            "insights": None,
        }

    # Convert ORM objects to plain dicts for the analysis module
    entry_dicts = [
        {
            "study_hours": e.study_hours,
            "sleep_hours": e.sleep_hours,
            "screen_time": e.screen_time,
            "mood": e.mood,
            "date": str(e.date),
        }
        for e in entries
    ]

    # Compute statistics (pure function, no side effects)
    stats = compute_stats(entry_dicts)

    # Generate AI insights from Claude
    insights = await generate_insights(stats)

    return {
        "status": "success",
        "stats": stats,
        "insights": insights,
        "history": entry_dicts,
    }


@app.get("/export")
def export_data(
    current_user: User = Depends(get_current_active_user),
    _rate_limit: bool = Depends(get_limiter_dependency("export_data")),
    db: Session = Depends(get_db)
):
    """
    Download all user's life data as a CSV file.
    
    Useful for:
    - Personal backup
    - External analysis in Excel/Python
    - Data portability (GDPR compliance)
    """
    logger.info(f"User {current_user.username} requested data export")
    
    # Fetch all entries for the current user
    entries = db.query(LifeData).filter(
        LifeData.user_id == current_user.id
    ).order_by(LifeData.date.asc()).all()
    
    if not entries:
        logger.warning(f"Export requested by {current_user.username} but no data found")
        raise HTTPException(
            status_code=404,
            detail="No data to export. Add some entries first."
        )
    
    # Create CSV in memory
    output = io.StringIO()
    writer = csv.DictWriter(
        output,
        fieldnames=["Date", "Study Hours", "Sleep Hours", "Screen Time", "Mood"]
    )
    
    writer.writeheader()
    for entry in entries:
        writer.writerow({
            "Date": str(entry.date),
            "Study Hours": entry.study_hours,
            "Sleep Hours": entry.sleep_hours,
            "Screen Time": entry.screen_time,
            "Mood": entry.mood
        })
    
    # Convert string to bytes for streaming
    output.seek(0)
    
    logger.info(f"Exported {len(entries)} entries for user {current_user.username}")
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=life_dashboard_{current_user.username}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv"
        }
    )

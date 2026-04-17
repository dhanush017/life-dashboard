#!/usr/bin/env python3
"""
Production startup script for Life Dashboard.
Configures environment and starts Uvicorn server.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check required environment variables
required_vars = ["GROQ_API_KEY", "SECRET_KEY", "DATABASE_URL"]
missing = [var for var in required_vars if not os.getenv(var)]

if missing:
    print(f"❌ Missing required environment variables: {', '.join(missing)}")
    sys.exit(1)

# Validate SECRET_KEY is not the default
if os.getenv("SECRET_KEY") == "your-super-secret-key-change-this-in-production":
    print("❌ ERROR: You must change SECRET_KEY in .env for production!")
    sys.exit(1)

# Set production environment
os.environ["ENVIRONMENT"] = "production"

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Start Uvicorn
port = os.getenv("PORT", "8000")
workers = os.getenv("WORKERS", "4")

cmd = [
    "uvicorn",
    "main:app",
    "--host", "0.0.0.0",
    "--port", port,
    "--workers", workers,
    "--access-log",
    "--no-server-header",  # Security: hide server info
]

print(f"🚀 Starting Life Dashboard in production mode")
print(f"   Port: {port}")
print(f"   Workers: {workers}")
print(f"   Database: {os.getenv('DATABASE_URL').split('@')[1] if '@' in os.getenv('DATABASE_URL', '') else 'SQLite'}")
print()

try:
    subprocess.run(cmd, check=True)
except KeyboardInterrupt:
    print("\n✋ Gracefully shutting down...")
    sys.exit(0)
except Exception as e:
    print(f"❌ Failed to start server: {e}")
    sys.exit(1)

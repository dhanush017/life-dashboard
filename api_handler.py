"""
Vercel serverless function handler for FastAPI
This wraps the FastAPI app for Vercel deployment
"""

from main import app

# Vercel's Python runtime requires exporting the ASGI app directly
# The vercel.json routes all requests to this handler
handler = app

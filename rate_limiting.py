"""
rate_limiting.py — Simple in-memory rate limiting for API endpoints.

Tracks request counts per IP address to prevent abuse.
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
from fastapi import Request, HTTPException, status
import asyncio

# Store request counts: {ip_address: [(timestamp, endpoint), ...]}
request_log: Dict[str, list] = {}

# Rate limiting rules (requests per minute)
RATE_LIMITS = {
    "add_data": (10, 60),        # 10 requests per 60 seconds
    "get_insights": (5, 60),     # 5 requests per 60 seconds
    "export_data": (3, 60),      # 3 requests per 60 seconds
    "auth": (5, 60),             # 5 requests per 60 seconds
}


async def check_rate_limit(request: Request, endpoint: str) -> bool:
    """
    Check if the client has exceeded rate limit for the given endpoint.
    
    Returns:
        True if within limits, False if rate limit exceeded
    """
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.now()
    limit, window = RATE_LIMITS.get(endpoint, (100, 60))
    
    # Initialize IP if not seen before
    if client_ip not in request_log:
        request_log[client_ip] = []
    
    # Remove old requests outside the time window
    cutoff_time = now - timedelta(seconds=window)
    request_log[client_ip] = [
        (timestamp, ep) for timestamp, ep in request_log[client_ip]
        if timestamp > cutoff_time and ep == endpoint
    ]
    
    # Check if limit exceeded
    if len(request_log[client_ip]) >= limit:
        return False
    
    # Add current request
    request_log[client_ip].append((now, endpoint))
    return True


def get_limiter_dependency(endpoint: str):
    """
    Factory function to create a rate limit dependency.
    Usage: Depends(get_limiter_dependency("add_data"))
    """
    async def rate_limit_check(request: Request):
        if not await check_rate_limit(request, endpoint):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {RATE_LIMITS[endpoint][0]} requests per {RATE_LIMITS[endpoint][1]} seconds."
            )
        return True
    return rate_limit_check


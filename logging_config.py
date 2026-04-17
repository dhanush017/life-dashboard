"""
logging_config.py — Centralized logging configuration for Life Dashboard.

Sets up structured logging with both file and console output.
All errors are logged for debugging and monitoring.
"""

import logging
import logging.handlers
import os
from datetime import datetime

# Create logs directory if it doesn't exist
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Define log file paths
ERROR_LOG = os.path.join(LOG_DIR, "error.log")
APP_LOG = os.path.join(LOG_DIR, "app.log")

# Configure root logger
logger = logging.getLogger("lifedashboard")
logger.setLevel(logging.DEBUG)

# Create formatters
detailed_formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

simple_formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# Console handler (INFO level and above)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(simple_formatter)
logger.addHandler(console_handler)

# File handler for all messages (DEBUG level)
file_handler = logging.handlers.RotatingFileHandler(
    APP_LOG,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)
logger.addHandler(file_handler)

# File handler for errors only
error_handler = logging.handlers.RotatingFileHandler(
    ERROR_LOG,
    maxBytes=5 * 1024 * 1024,  # 5MB
    backupCount=5
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(detailed_formatter)
logger.addHandler(error_handler)


def get_logger(name: str = "lifedashboard"):
    """Get a logger instance."""
    return logging.getLogger(name)

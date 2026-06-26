"""
Centralized logging configuration.

Every module should import the logger from here.

Example:
    from utils.logger import get_logger

    logger = get_logger(__name__)
"""

import logging
from pathlib import Path

# Create logs directory if it doesn't exist

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_DIR = PROJECT_ROOT/ "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# Configure root logger

logging.basicConfig(level=logging.INFO, format=(
        "%(asctime)s | "
        "%(levelname)-8s | "
        "%(name)s | "
        "%(message)s"
    ),
    datefmt="%Y-%m-%d %H:%M:%S", handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


def get_logger(name: str) -> logging.Logger:
    """
    Returns a logger instance.

    Parameters
    ----------
    name : str
        Usually __name__

    Returns
    -------
    logging.Logger
    """
    return logging.getLogger(name)
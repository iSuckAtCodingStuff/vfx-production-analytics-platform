"""Logging configuration for the VFX Production Analytics Platform.
Creates a reusable logger that writes to both the console
and a log file"""

import logging

from pipeline.config import LOG_DIR

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


def get_logger(name: str = "vfx_pipeline") -> logging.Logger:
    """Create and return a configured logger

    Parameters
    ----------
    name : str
        Logger name.

    Returns
    -------
    logging.Logger"""

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    logger.propagate = False

    formatter = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S",)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
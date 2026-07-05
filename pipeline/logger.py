"""Logging configuration for the VFX Production Analytics Platform.
Creates a reusable logger that writes to both the console
and a log file"""

from __future__ import annotations

import logging
from datetime import datetime

import pandas as pd

from pipeline.config import LOG_DIR, INVALID_LOG_DIR

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"

RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

INVALID_LOG_FILE = (INVALID_LOG_DIR / f"invalid_rows_{RUN_TIMESTAMP}.csv")


# ============================================================================
# Logging Configuration
# ============================================================================


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


def log_invalid_rows(dataframe: pd.DataFrame, table_name: str, validation: str, reason: str, ) -> None:
    """ Append invalid rows to the current ETL run log.
    Args:
        dataframe: Invalid rows.
        table_name: Source table.
        validation: Validation rule.
        reason: Reason the rows were rejected """

    if dataframe.empty:
        return

    invalid = dataframe.copy()

    invalid.insert(0, "rejected_at", datetime.now(),)

    invalid.insert(1, "table_name", table_name,)

    invalid.insert(2, "validation", validation,)

    invalid.insert(3, "reason", reason,)

    invalid.to_csv(INVALID_LOG_FILE, mode="a", header=not INVALID_LOG_FILE.exists(), index=False,)
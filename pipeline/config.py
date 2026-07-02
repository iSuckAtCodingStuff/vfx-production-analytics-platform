""" Configuration settings for the VFX Production Analytics Platform.
    Loads database credentials from environment variables. """

from pathlib import Path
from dotenv import load_dotenv
import os

# Load .env from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

RAW_SCHEMA = "raw"
STAGING_SCHEMA = "staging"
WAREHOUSE_SCHEMA = "warehouse"

LOG_DIR = BASE_DIR / "logs"
DATA_DIR = BASE_DIR / "data"

print(DB_CONFIG)
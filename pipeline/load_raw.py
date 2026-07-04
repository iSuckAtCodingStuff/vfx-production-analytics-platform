""" Load CSV files from the data directory into the PostgreSQL raw schema.

This module performs a full refresh of the raw layer by truncating each
destination table and loading the corresponding CSV data """

# import required libraries

from pathlib import Path
import sys
import time

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from pipeline.config import DATA_DIR
from pipeline.db import get_engine
from pipeline.logger import get_logger

RAW_SCHEMA = "raw"

logger = get_logger(__name__)

engine = get_engine()

def truncate_table(schema: str, table_name: str) -> None:
    """ Remove all rows from a table while preserving its structure,
    constraints, indexes, and permissions """

    query = text(f"TRUNCATE TABLE {schema}.{table_name};")

    try:
        with engine.begin() as connection:
            connection.execute(query)

        logger.info(f"Truncated table: {schema}.{table_name}")

    except SQLAlchemyError:
        logger.exception(f"Failed to truncate table: {schema}.{table_name}")
        raise


def table_exists(schema: str, table_name: str) -> bool:
    """Check whether a table exists in the specified schema."""

    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = :schema
              AND table_name = :table_name
        );
    """)

    with engine.connect() as connection:
        exists = connection.execute(query, {"schema": schema, "table_name": table_name}).scalar()

    return bool(exists)
    

def load_table(csv_path: Path, schema: str) -> int:
    """ Load a CSV file into a PostgreSQL table.
    The table name is inferred from the CSV filename.
    Existing data is removed before loading fresh data.
    Returns:
        int: Number of rows loaded.
    """

    table_name = csv_path.stem

    if not table_exists(schema, table_name):
        raise ValueError(f"Destination table '{schema}.{table_name}' does not exist.")

    logger.info(f"Loading {csv_path.name} into {schema}.{table_name}")

    try:
        # Read the CSV
        df = pd.read_csv(csv_path)

        # Remove existing data
        truncate_table(schema, table_name)

        # Append new data
        df.to_sql(
            name=table_name,
            con=engine,
            schema=schema,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1000
        )

        row_count = len(df)

        logger.info(f"Successfully loaded {row_count:,} rows into "f"{schema}.{table_name}")

        return row_count

    except FileNotFoundError:
        logger.exception(f"CSV file not found: {csv_path}")
        raise

    except pd.errors.EmptyDataError:
        logger.exception(f"CSV file is empty: {csv_path}")
        raise

    except SQLAlchemyError:
        logger.error(f"Database error while loading {schema}.{table_name}")
        raise

    except Exception:
        logger.exception(f"Unexpected error while loading {csv_path.name}")
        raise


def main() -> None:
    """ Discover and load all CSV files into the raw schema.
    Logs execution statistics and continues processing
    if an individual file fails """

    logger.info("Starting raw data load...")

    start_time = time.perf_counter()

    success_count = 0
    failure_count = 0
    total_rows = 0
    
    failed_files = {}

    csv_files = sorted(DATA_DIR.glob("*.csv"))

    if not csv_files:
        logger.warning(f"No CSV files found in {DATA_DIR}")
        return

    for csv_file in csv_files:
        try:
            rows = load_table(csv_file, schema=RAW_SCHEMA)

            success_count += 1
            total_rows += rows

        except Exception as e:
            failure_count += 1
            failed_files[csv_file.name] = type(e).__name__

            logger.error(f"Failed to load {csv_file.name}: " f"{type(e).__name__}")
            continue


    elapsed = time.perf_counter() - start_time

    logger.info("=" * 50)
    logger.info("RAW LOAD SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Files discovered : {len(csv_files)}")
    logger.info(f"Files loaded     : {success_count}")
    logger.info(f"Files failed     : {failure_count}")
    logger.info(f"Rows loaded      : {total_rows:,}")
    logger.info(f"Elapsed time     : {elapsed:.2f} seconds")
    logger.info("=" * 50)

    if failed_files:
        logger.info("Failed files:")

        for file_name, error in failed_files.items():
            logger.info(f" - {file_name}: {error}")
     
    logger.info("=" * 50)

    if failure_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
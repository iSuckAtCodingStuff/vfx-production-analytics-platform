""" Transform data from the raw schema into the staging schema.

This module reads data from the raw schema, applies data cleaning
and standardization rules, and loads the transformed data into the
staging schema.

The raw schema is never modified.
The staging tables are rebuilt on each run """

from __future__ import annotations

import sys
import time

import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from pipeline.config import DB_CONFIG
from pipeline.db import get_engine
from pipeline.logger import get_logger, log_invalid_rows


# ============================================================================
# Constants
# ============================================================================

RAW_SCHEMA = "raw"
STAGING_SCHEMA = "staging"


# ============================================================================
# Logger
# ============================================================================

logger = get_logger(__name__)


# ============================================================================
# Database Engine
# ============================================================================

engine = get_engine()


# ============================================================================
# Helper Functions
# ============================================================================

def truncate_table(schema: str, table_name: str) -> None:
    """ Truncate a table before loading transformed data.
    Args:
        schema: Database schema.
        table_name: Name of the table to truncate """

    query = text(f"TRUNCATE TABLE {schema}.{table_name};")

    with engine.begin() as connection:
        connection.execute(query)


def read_table(schema: str, table_name: str) -> pd.DataFrame:
    """ Read a database table into a pandas DataFrame.
    Args:
        schema: Source schema.
        table_name: Table to read.

    Returns:
        DataFrame containing the table data """

    query = text(f"SELECT * FROM {schema}.{table_name};")

    return pd.read_sql(query, engine)


def write_table(dataframe: pd.DataFrame, schema: str, table_name: str, ) -> int:
    """ Replace the contents of a staging table with a DataFrame.

    Args:
        dataframe: DataFrame to load.
        schema: Destination schema.
        table_name: Destination table.

    Returns:
        Number of rows written """

    truncate_table(schema, table_name)

    dataframe.to_sql(
        table_name,
        engine,
        schema=schema,
        if_exists="append",
        index=False,
    )

    return len(dataframe)


def clean_text_columns(dataframe: pd.DataFrame, columns: list[str], ) -> pd.DataFrame:
    """ Trim leading and trailing whitespace from text columns.
    Args:
        dataframe: DataFrame to clean.
        columns: List of text columns.

    Returns:
        Cleaned DataFrame """

    for column in columns:
        dataframe[column] = dataframe[column].str.strip()

    return dataframe


def normalize_title_columns(dataframe: pd.DataFrame, columns: list[str], ) -> pd.DataFrame:
    """ Normalize text columns to title case.

    Args:
        dataframe: DataFrame to clean.
        columns: Columns to normalize.

    Returns:
        Cleaned DataFrame """

    for column in columns:
        dataframe[column] = (dataframe[column].str.strip().str.title())

    return dataframe


def replace_blank_strings(dataframe: pd.DataFrame, ) -> pd.DataFrame:
    """ Replace blank strings with NULL values.
    Args:
        dataframe: DataFrame to clean.

    Returns:
        Cleaned DataFrame """

    dataframe.replace(r"^\s*$", pd.NA, regex=True, inplace=True,)

    return dataframe


def validate_date_range(dataframe: pd.DataFrame, start_column: str, end_column: str, ) -> pd.DataFrame:
    """ Remove rows where both dates exist and the end date
    occurs before the start date.
    Args:
        dataframe: DataFrame to validate.
        start_column: Name of the start date column.
        end_column: Name of the end date column.

    Returns:
        Validated DataFrame """

    mask = (dataframe[start_column].isna() | dataframe[end_column].isna() | (dataframe[end_column] >= dataframe[start_column]))

    return dataframe.loc[mask]


def transform_projects() -> int:
    """ Transform the projects table from the raw schema
    into the staging schema.

    Returns:
        Number of rows loaded into the staging table """

    df = read_table(RAW_SCHEMA, "projects", )

    df = replace_blank_strings(df)

    df = clean_text_columns(df,
        [
            "project_name",
            "client",
        ],
    )

    df = normalize_title_columns(df, 
        [
            "project_type",
            "complexity",
            "status",
        ],
    )

    df = validate_date_range(df, "start_date", "end_date", )

    df = df.drop_duplicates()

    return write_table(df, STAGING_SCHEMA, "projects", )


# ============================================================================
# Transformation Pipeline
# ============================================================================

TRANSFORMATIONS = [("projects", transform_projects), ]

# ============================================================================
# Main
# ============================================================================

def main() -> None:
    """ Execute the transformation pipeline """

    start_time = time.perf_counter()

    logger.info("Starting transformation pipeline...")

    total_rows = 0
    success_count = 0
    failure_count = 0

    failed_tables = {}

    for table_name, transform in TRANSFORMATIONS:

        logger.info(f"Transforming {table_name}...")

        try:
            rows = transform()

            total_rows += rows
            success_count += 1

            logger.info(f"Successfully transformed "f"{table_name} ({rows} rows).")

        except Exception as e:

            failure_count += 1

            failed_tables[table_name] = type(e).__name__

            logger.exception(f"Failed transforming {table_name}")

            continue

    elapsed = time.perf_counter() - start_time

    logger.info("=" * 60)
    logger.info("Transformation Summary")
    logger.info("=" * 60)

    logger.info(f"Tables transformed : {success_count}")

    logger.info(f"Tables failed : {failure_count}")

    logger.info(f"Rows loaded : {total_rows}")

    logger.info(f"Elapsed time : {elapsed:.2f} seconds")

    if failed_tables:
        logger.info("")

        logger.info("Failed Tables:")

        for table, error in failed_tables.items():
            logger.info(f"{table} : {error}")

    if failure_count:

        sys.exit(1)

if __name__ == "__main__":
    main()

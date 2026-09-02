"""
PostgreSQL RAW → GCS RAW exporter.

Exports PostgreSQL RAW tables as Parquet to GCS.

Event tables:
    - Partitioned by business year/month.
    - Each table uses its own business-date column.

Entity tables:
    - Exported as complete snapshots.
"""

from datetime import date
import calendar

import pandas as pd
from google.cloud import storage

from pipeline.config import (
    GCS_BUCKET_NAME,
    GCS_RAW_PREFIX
)

from pipeline.db import get_engine, dispose_engine

# ---------------------------------------------------------------------------
# Export configuration
# ---------------------------------------------------------------------------

EXPORT_CONFIG = {
    "timesheets": {
        "date_column": "work_date",
        "category": "events",
    },
    "task_assignments": {
        "date_column": "assignment_date",
        "category": "events",
    },
    "render_jobs": {
        "date_column": "submission_date",
        "category": "events",
    },
    "deliveries": {
        "date_column": "delivery_date",
        "category": "events",
    },
    "projects": {
        "date_column": "start_date",
        "category": "entities",
    },
    "sequences": {
        "date_column": "start_date",
        "category": "entities",
    },
    "shots": {
        "date_column": "start_date",
        "category": "entities",
    },
    "tasks": {
        "date_column": "start_date",
        "category": "entities",
    },
    "artists": {
        "date_column": None,
        "category": "entities",
    },
}


# ----------------------------------------------------------------------
# GCS upload helper
# ----------------------------------------------------------------------

def upload_parquet(df: pd.DataFrame, partition_path: str, ) -> None:
    """
    Convert a DataFrame to Parquet and upload it to GCS.
    """

    parquet_bytes = df.to_parquet(index=False, engine="pyarrow")

    client = storage.Client()

    bucket = client.bucket(GCS_BUCKET_NAME)

    blob = bucket.blob(partition_path)

    blob.upload_from_string(parquet_bytes, content_type="application/octet-stream",)

    print(
        f"Upload successful:\n"
        f"gs:/{GCS_BUCKET_NAME}/{partition_path}"
    )
    

# ----------------------------------------------------------------------
# Event table exporter
# ----------------------------------------------------------------------

def export_event_table(table_name: str, date_column: str) -> None:
    """
    Export an event table from PostgreSQL RAW to
    monthly-partitioned Parquet files in GCS.
    """

    engine = get_engine()

    try:

        query = f"""
            SELECT *
            FROM raw.{table_name}
            ORDER BY 1;
        """

        df = pd.read_sql(query, engine)

        print(
            f"\nExtracted {len(df):,} rows "
            f"from raw.{table_name}"
        )

        if df.empty:
            print("No records found. Nothing will be uploaded.")
            return

        # --------------------------------------------------------------
        # Ensure business date is a proper datetime
        # --------------------------------------------------------------

        df[date_column] = pd.to_datetime(
            df[date_column],
            errors="coerce",
        )

        invalid_dates = df[date_column].isna().sum()

        if invalid_dates:
            print(
                f"WARNING: {invalid_dates:,} rows have "
                f"invalid {date_column} values."
            )

        # --------------------------------------------------------------
        # Create year/month partition columns
        # --------------------------------------------------------------

        df["_partition_year"] = df[date_column].dt.year
        df["_partition_month"] = df[date_column].dt.month

        # --------------------------------------------------------------
        # Upload one Parquet file per month
        # --------------------------------------------------------------

        for (year, month), monthly_df in df.groupby(
            ["_partition_year", "_partition_month"], 
            dropna=True
        ):

            year = int(year)
            month = int(month)

            monthly_df = monthly_df.drop(columns=["_partition_year", "_partition_month"])

            partition_path = (
                f"{GCS_RAW_PREFIX}/"
                f"events/{table_name}/"
                f"year={year}/"
                f"month={month:02d}/"
                f"data.parquet"
            )

            print(
                f"Uploading {table_name}: "
                f"{year}-{month:02d} "
                f"({len(monthly_df):,} rows)"
            )

            upload_parquet(
                monthly_df,
                partition_path,
            )

    finally:
        dispose_engine()


# ----------------------------------------------------------------------
# Event Monthly event table exporter
# ----------------------------------------------------------------------

def export_event_table_month(table_name: str, date_column: str, year:int, month:int) -> None:
    """
    Export one calendar month from a RAW event table to GCS.
    """
    engine = get_engine()

    try:
        first_day = date(year, month, 1)

        last_day = date(year, month, calendar.monthrange(year, month)[1],)

        query = f"""
            select *
            from raw.{table_name}
            where {date_column}::date >= %(start_date)s
                and {date_column}::date <= %(end_date)s
            order by 1;    
        """

        df = pd.read_sql(query, engine, params={
            "start_date": first_day,
            "end_date": last_day
        },
        )

        print(
            f"Extracted {len(df):,} rows "
            f"from raw.{table_name} "
            f"for {year}-{month:02d}"
        )

        if df.empty:
            print(
                f"No records found for "
                f"{table_name} {year}-{month:02d}"
            )
            return

        partition_path = (
            f"{GCS_RAW_PREFIX}/"
            f"events/{table_name}/"
            f"year={year}/"
            f"month={month:02d}/"
            f"data.parquet"
        )

        upload_parquet(
            df,
            partition_path,
        )

    finally:
        dispose_engine()

# ----------------------------------------------------------------------
# Entity table exporter
# ----------------------------------------------------------------------

def export_entity_table(table_name: str,) -> None:
    """
    Export an entity table as a complete RAW snapshot.
    """

    engine = get_engine()

    try:

        query = f"""
            SELECT *
            FROM raw.{table_name}
            ORDER BY 1;
        """

        df = pd.read_sql(query, engine)

        print(
            f"\nExtracted {len(df):,} rows "
            f"from raw.{table_name}"
        )

        if df.empty:
            print("No records found. Nothing will be uploaded.")
            return

        partition_path = (
            f"{GCS_RAW_PREFIX}/"
            f"entities/{table_name}/"
            f"data.parquet"
        )

        upload_parquet(
            df,
            partition_path,
        )

    finally:
        dispose_engine()


# ----------------------------------------------------------------------
# Generic table exporter
# ----------------------------------------------------------------------

def export_table(
    table_name: str,
) -> None:
    """
    Export a configured RAW table to GCS.
    """

    if table_name not in EXPORT_CONFIG:
        raise ValueError(
            f"Unsupported table: {table_name}. "
            f"Supported tables: {', '.join(EXPORT_CONFIG)}"
        )

    config = EXPORT_CONFIG[table_name]

    if config["category"] == "events":

        export_event_table(
            table_name=table_name,
            date_column=config["date_column"],
        )

    else:

        export_entity_table(
            table_name=table_name,
        )

# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

if __name__ == "__main__":

    for table_name in EXPORT_CONFIG:

        print(
            "\n"
            + "=" * 70
            + f"\nExporting: {table_name}"
            + "\n"
            + "=" * 70
        )

        export_table(table_name)
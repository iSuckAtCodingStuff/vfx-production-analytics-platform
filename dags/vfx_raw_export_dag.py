"""
Airflow DAG for VFX Production Analytics RAW ingestion.

Pipeline:

PostgreSQL RAW
      ↓
GCS RAW
"""

from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator

from datetime import datetime


def export_monthly_raw(**context):
    """
    Export the month represented by Airflow's logical date.
    """

    logical_date = context["logical_date"]

    year = logical_date.year
    month = logical_date.month

    print(
        f"Processing RAW data for "
        f"{year}-{month:02d}"
    )

    # Temporary proof-of-concept.
    #
    # We'll connect this to the actual exporter
    # after confirming the Airflow date semantics.

    print(f"Year: {year}")
    print(f"Month: {month:02d}")

with DAG(
    dag_id = 'vfx_raw_export',
    description= 'Monthly PostgreSQL RAW → GCS RAW ingestion',
    start_date= datetime(2026, 1, 1),
    schedule= '@monthly',
    catchup= False,
    tags=["vfx", "raw", "gcs"]
)as dag:

    export_raw_task = PythonOperator(
        task_id = "export_raw_data",
        python_callable= export_monthly_raw,
    )
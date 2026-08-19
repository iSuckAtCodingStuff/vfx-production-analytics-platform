""" load_warehouse.py

Orchestrates the Warehouse ETL process.

Pipeline
--------
Staging
    ↓
Warehouse Dimensions
    ↓
Warehouse Facts """

# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------

from pipeline.db import get_engine, dispose_engine
from pipeline.logger import get_logger

from pipeline.warehouse_loader import (
    truncate_warehouse_tables,
    load_dim_project,
    load_dim_sequence,
    load_dim_shot,
    load_dim_task,
    load_dim_artist,
    load_dim_date,
    load_fact_task_assignment,
    load_fact_timesheet,
    load_fact_render,
    load_fact_delivery
)

# ---------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------

logger = get_logger()

# ---------------------------------------------------------------------
# Load Dimensions
# ---------------------------------------------------------------------

DIMENSION_LOADERS = (
    load_dim_project,
    load_dim_sequence,
    load_dim_shot,
    load_dim_task,
    load_dim_artist,
    load_dim_date,
)

# ---------------------------------------------------------------------
# Load Facts
# ---------------------------------------------------------------------

FACT_LOADERS = (
    load_fact_task_assignment,
    load_fact_timesheet,
    load_fact_render,
    load_fact_delivery,
)

def main() -> None:
    """ Execute the Warehouse ETL pipeline """

    logger.info("=" * 80)
    logger.info("Starting Warehouse ETL")
    logger.info("=" * 80)
    
    engine = get_engine()

    try:
        with engine.begin() as connection:
            truncate_warehouse_tables(connection)

            for loader in DIMENSION_LOADERS:
                loader(connection)

            for loader in FACT_LOADERS:
                loader(connection)

            logger.info("=" * 80)
            logger.info("Warehouse ETL completed successfully.")
            logger.info("=" * 80)

    except Exception:
        logger.exception(f"Warehouse ETL failed.")
        raise

    finally:
        dispose_engine()

if __name__ == "__main__":
    main()
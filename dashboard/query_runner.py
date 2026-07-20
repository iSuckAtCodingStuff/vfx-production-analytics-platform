from pathlib import Path

import pandas as pd
from sqlalchemy import text

from pipeline.db import get_engine


def load_sql(relative_path: str) -> str:
    """Read a SQL file from the analytics directory"""

    project_root = Path(__file__).resolve().parent.parent
    sql_path = project_root / "analytics" / relative_path

    with open(sql_path, "r", encoding="utf-8") as file:
        return file.read()


def execute_sql(relative_path: str) -> pd.DataFrame:
    """ Execute an analytical SQL report and return the result as a Pandas DataFrame.
    Args:
        relative_path: Relative path to the SQL file within the analytics directory.
    Returns:
        Query results as a Pandas DataFrame. """

    query = load_sql(relative_path)

    engine = get_engine()

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)
    


if __name__ == "__main__":

    df = execute_sql("executive_dashboard/40_studio_kpi_dashboard.sql")

    print(df)
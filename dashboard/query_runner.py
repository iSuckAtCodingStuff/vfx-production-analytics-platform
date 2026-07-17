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
    """Execute a SQL file and return a Pandas DataFrame"""

    query = load_sql(relative_path)

    engine = get_engine()

    with engine.connect() as connection:
        return pd.read_sql(text(query), connection)
    

def execute_scalar(relative_path: str):
    """Execute a SQL file that returns a single value."""

    df = execute_sql(relative_path)

    return df.iloc[0, 0]

if __name__ == "__main__":

    df = execute_sql(
        "project_metrics/total_projects.sql"
    )

    print(df)
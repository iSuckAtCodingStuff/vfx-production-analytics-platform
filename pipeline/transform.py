"""
===========================================================
VFX Production Analytics Platform
Raw -> Staging Transformation Pipeline

Purpose:
    Cleans, validates and lightly normalizes raw production
    data before loading it into the staging schema
===========================================================
"""
import json
import pandas as pd
from sqlalchemy import text

from pipeline.logger import get_logger
from pipeline.db import get_engine, dispose_engine

logger = get_logger(__name__)

INVALID_ROW_COUNT = 0

# ==========================================================
# Staging Column Definitions
# ==========================================================

STAGING_COLUMNS = {
    "projects": [
        "project_id",
        "project_name",
        "project_type",
        "client",
        "budget_million_usd",
        "complexity",
        "start_date",
        "end_date",
        "status",
        "_loaded_at",
    ],

    "sequences": [
        "sequence_id",
        "project_id",
        "sequence_name",
        "complexity",
        "start_date",
        "end_date",
        "status",
        "_loaded_at",
    ],

    "shots": [
        "shot_id",
        "sequence_id",
        "shot_name",
        "complexity",
        "frame_count",
        "start_date",
        "end_date",
        "status",
        "_loaded_at",
    ],

    "tasks": [
        "task_id",
        "shot_id",
        "department",
        "estimated_hours",
        "priority",
        "start_date",
        "end_date",
        "status",
        "_loaded_at",
    ],

    "artists": [
        "artist_id",
        "artist_name",
        "department",
        "experience_years",
        "_loaded_at",
    ],

    "task_assignments": [
        "assignment_id",
        "task_id",
        "artist_id",
        "assigned_hours",
        "assignment_date",
        "_loaded_at",
    ],

    "timesheets": [
        "timesheet_id",
        "assignment_id",
        "work_date",
        "hours_logged",
        "_loaded_at",
    ],

    "render_jobs": [
        "render_id",
        "shot_id",
        "frame_count",
        "render_engine",
        "render_status",
        "render_hours",
        "submission_date",
        "completion_date",
        "_loaded_at",
    ],

    "deliveries": [
        "delivery_id",
        "shot_id",
        "version",
        "delivery_date",
        "client_status",
        "review_days",
        "final_delivery",
        "_loaded_at",
    ],
}

ID_PATTERNS = {
    "project_id": r"^P\d+$",
    "sequence_id": r"^SQ\d+$",
    "shot_id": r"^SH\d+$",
    "task_id": r"^T\d+$",
    "artist_id": r"^A\d+$",
    "assignment_id": r"^TA\d+$",
    "timesheet_id": r"^TS\d+$",
    "render_id": r"^R\d+$",
    "delivery_id": r"^D\d+$",
    "version": r"^V\d+$",
}


# ==========================================================
# Logging Helper
# ==========================================================

def log_invalid_rows(table_name: str, invalid_df: pd.DataFrame, reason: str, engine) -> None:
    """ Log invalid rows removed during transformation """

    global INVALID_ROW_COUNT

    INVALID_ROW_COUNT += len(invalid_df)

    if invalid_df.empty:
        return

    logger.warning("%s: Removed %d invalid row(s). Reason: %s", table_name, len(invalid_df), reason,)

    if invalid_df.empty:
        return
    
    records = invalid_df.to_dict(orient="records")

    for record in records:
        for key, value in record.items():
            if pd.isna(value):
                record[key] = None

    invalid_log = pd.DataFrame(
        {
            "source_table": [table_name] * len(records),
            "error_reason": [reason] * len(records),
            "row_data": [json.dumps(record, default=str) for record in records],
        }
    )

    try:
        invalid_log.to_sql(name="invalid_log", schema="staging", con=engine,if_exists="append", index=False,)
    
    except Exception:
        logger.exception("Failed to write rejected rows to staging.invalid_log")

    logger.debug("%s\n%s", reason, invalid_df.to_string(index=False),)


# ==========================================================
# Generic Validation Helper
# ==========================================================

def _apply_validation(df: pd.DataFrame, mask: pd.Series, table_name: str, reason: str, engine) -> pd.DataFrame:
    """ Apply a validation mask, log rejected rows, and return only valid rows """

    invalid_rows = df.loc[~mask]
    if not invalid_rows.empty:
        log_invalid_rows(table_name, invalid_rows, reason, engine)
    
    return df.loc[mask].copy()


# ==========================================================
# Generic Cleaning Helpers
# ==========================================================

def normalize_text_columns(df: pd.DataFrame, columns: list[str],) -> pd.DataFrame:
    """ Trim whitespace from text columns """

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = (df[column].str.strip())

    return df


def convert_numeric_columns(df: pd.DataFrame,columns: list[str],) -> pd.DataFrame:
    """ Convert numeric columns while preserving invalid
    values as NaN for later validation """

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce",)

    return df


def convert_date_columns(df: pd.DataFrame, columns: list[str],) -> pd.DataFrame:
    """ Convert date columns to pandas datetime Invalid values become NaT """

    df = df.copy()

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce",)

    return df


def select_staging_columns(df: pd.DataFrame, table_name: str,) -> pd.DataFrame:
    """ Return only the columns required by the staging schema """

    return df[STAGING_COLUMNS[table_name]].copy()


# ==========================================================
# Database Helper
# ==========================================================

def truncate_staging_table(table_name: str, engine) -> None:
    """ Truncate a staging table before loading """

    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE staging.{table_name} CASCADE;"))


# ==========================================================
# Validation Helpers
# ==========================================================

def validate_required_columns(df: pd.DataFrame, columns: list[str], table_name: str, engine) -> pd.DataFrame:
    """ Remove rows containing NULL values in required columns """

    for column in columns:
        mask = df[column].notna()

        df = _apply_validation(df, mask, table_name, f"{column} cannot be NULL", engine)

    return df


def validate_numeric(df: pd.DataFrame, column: str, table_name: str,engine) -> pd.DataFrame:
    """ Remove rows where numeric conversion failed """

    mask = df[column].notna()

    return _apply_validation(df, mask, table_name, f"{column} contains non-numeric value", engine)


def validate_non_negative(df: pd.DataFrame, column: str, table_name: str, engine) -> pd.DataFrame:
    """ Remove rows containing negative values """

    mask = df[column] >= 0

    return _apply_validation(df, mask, table_name, f"{column} cannot be negative", engine)


def validate_positive( df: pd.DataFrame, column: str, table_name: str, engine) -> pd.DataFrame:
    """ Remove rows containing values less than or equal to zero """

    mask = df[column] > 0

    return _apply_validation(df, mask,table_name, f"{column} must be greater than zero", engine)


def validate_date_order(df: pd.DataFrame,start_column: str, end_column: str,table_name: str, engine) -> pd.DataFrame:
    """ Validate chronological order between two dates """

    mask = df[end_column] >= df[start_column]

    return _apply_validation(df, mask, table_name, f"{end_column} cannot be earlier than {start_column}", engine)


def validate_regex(df: pd.DataFrame, column: str, pattern: str, table_name: str, engine) -> pd.DataFrame:
    """ Validate values using a regular expression """

    mask = df[column].str.match(pattern, na=False)

    return _apply_validation(df, mask, table_name, f"{column} has an invalid format", engine)


# ==========================================================
# Transformation Functions
# ==========================================================

def transform_projects(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the projects table """

    table_name = "projects"

    df = normalize_text_columns(df,
        [
            "project_id",
            "project_name",
            "project_type",
            "client",
            "complexity",
            "status",
        ],
    )

    df = convert_numeric_columns(df, ["budget_million_usd"],)

    df = convert_date_columns(df, ["start_date", "end_date"],)

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "project_id", ID_PATTERNS["project_id"], table_name, engine)

    df = validate_numeric(df, "budget_million_usd", table_name, engine)

    df = validate_non_negative(df, "budget_million_usd", table_name, engine)

    df = validate_date_order(df, "start_date", "end_date", table_name, engine)

    return select_staging_columns(df, table_name,)


def transform_sequences(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the sequences table     """

    table_name = "sequences"

    df = normalize_text_columns(df, ["sequence_id", "project_id", "sequence_name", "complexity", "status"],)

    df = convert_date_columns(df, ["start_date", "end_date"])

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "sequence_id", ID_PATTERNS["sequence_id"], table_name, engine)

    df = validate_date_order(df, "start_date", "end_date", table_name, engine)

    return select_staging_columns(df, table_name)


def transform_shots(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the shots table """

    table_name = "shots"

    df = normalize_text_columns(df, ["shot_id", "sequence_id", "shot_name", "complexity", "status"],)

    df = convert_numeric_columns(df, ["frame_count"])
    df = convert_date_columns(df, ["start_date", "end_date"])

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "shot_id", ID_PATTERNS["shot_id"], table_name, engine)

    df = validate_numeric(df, "frame_count", table_name, engine)
    df = validate_positive(df, "frame_count", table_name, engine)

    df = validate_date_order(df, "start_date", "end_date", table_name, engine)

    return select_staging_columns(df, table_name)


def transform_tasks(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the tasks table """

    table_name = "tasks"

    df = normalize_text_columns(df, ["task_id", "shot_id", "department", "priority", "status"],)

    df = convert_numeric_columns(df, ["estimated_hours"])
    df = convert_date_columns(df, ["start_date", "end_date"])

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "task_id", ID_PATTERNS["task_id"], table_name, engine)

    df = validate_numeric(df, "estimated_hours", table_name, engine)

    df = validate_non_negative(df, "estimated_hours", table_name, engine)

    df = validate_date_order(df, "start_date", "end_date", table_name, engine)

    return select_staging_columns(df, table_name)


def transform_artists(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the artists table """

    table_name = "artists"

    df = normalize_text_columns(df,
        [
            "artist_id",
            "artist_name",
            "department",
        ],
    )

    df = convert_numeric_columns(df, ["experience_years"],)

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "artist_id", ID_PATTERNS["artist_id"], table_name, engine)

    df = validate_numeric(df, "experience_years", table_name, engine)

    df = validate_non_negative(df, "experience_years", table_name, engine)

    return select_staging_columns(df, table_name,)


def transform_task_assignments(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the task_assignments table """

    table_name = "task_assignments"

    df = normalize_text_columns(df,
        [
            "assignment_id",
            "task_id",
            "artist_id",
        ],
    )

    df = convert_numeric_columns(df, ["assigned_hours"],)

    df = convert_date_columns(df, ["assignment_date"],)

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "assignment_id", ID_PATTERNS["assignment_id"], table_name, engine)

    df = validate_regex(df, "task_id", ID_PATTERNS["task_id"], table_name, engine)

    df = validate_regex(df, "artist_id", ID_PATTERNS["artist_id"], table_name, engine)

    df = validate_numeric(df, "assigned_hours", table_name, engine)

    df = validate_non_negative(df, "assigned_hours", table_name, engine)

    return select_staging_columns(df, table_name,)


def transform_timesheets(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the timesheets table """

    table_name = "timesheets"

    df = normalize_text_columns(df,
        [
            "timesheet_id",
            "assignment_id",
        ],
    )

    df = convert_numeric_columns(df, ["hours_logged"],)

    df = convert_date_columns(df, ["work_date"],)

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "timesheet_id", ID_PATTERNS["timesheet_id"], table_name, engine)

    df = validate_regex(df, "assignment_id", ID_PATTERNS["assignment_id"], table_name, engine)

    df = validate_numeric(df, "hours_logged", table_name, engine)

    df = validate_non_negative(df, "hours_logged", table_name, engine)

    return select_staging_columns(df, table_name,)


def transform_render_jobs(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the render_jobs table """

    table_name = "render_jobs"

    df = normalize_text_columns(df,
        [
            "render_id",
            "shot_id",
            "render_engine",
            "render_status",
        ],
    )

    df = convert_numeric_columns(df,
        [
            "frame_count",
            "render_hours",
        ],
    )

    df = convert_date_columns(df,
        [
            "submission_date",
            "completion_date",
        ],
    )

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "render_id", ID_PATTERNS["render_id"], table_name, engine)

    df = validate_regex(df, "shot_id", ID_PATTERNS["shot_id"], table_name, engine)

    df = validate_numeric(df, "frame_count", table_name, engine)

    df = validate_positive(df, "frame_count", table_name, engine)

    df = validate_numeric(df, "render_hours", table_name, engine)

    df = validate_non_negative(df, "render_hours", table_name, engine)

    df = validate_date_order(df, "submission_date", "completion_date", table_name, engine)

    return select_staging_columns(df, table_name, )


def transform_deliveries(df: pd.DataFrame, engine) -> pd.DataFrame:
    """ Transform the deliveries table """

    table_name = "deliveries"

    df = normalize_text_columns(df,
        [
            "delivery_id",
            "shot_id",
            "version",
            "client_status",
        ],
    )
    
    df = convert_numeric_columns(df, ["review_days"],)

    df = convert_date_columns(df, ["delivery_date"],) 

    df = validate_required_columns(df, STAGING_COLUMNS[table_name], table_name, engine)

    df = validate_regex(df, "delivery_id", ID_PATTERNS["delivery_id"], table_name, engine)

    df = validate_regex(df, "shot_id",ID_PATTERNS["shot_id"], table_name, engine)

    df = validate_regex(df, "version", ID_PATTERNS["version"], table_name, engine)

    df = validate_numeric(df, "review_days", table_name, engine)

    df = validate_non_negative(df, "review_days", table_name, engine)

    return select_staging_columns(df, table_name,)



# ==========================================================
# Transformation Mapping
# ==========================================================

TRANSFORMATIONS = {
    "projects": transform_projects,
    "sequences": transform_sequences,
    "shots": transform_shots,
    "tasks": transform_tasks,
    "artists": transform_artists,
    "task_assignments": transform_task_assignments,
    "timesheets": transform_timesheets,
    "render_jobs": transform_render_jobs,
    "deliveries": transform_deliveries,
}


# ==========================================================
# Database Load Helper
# ==========================================================

def load_to_staging(df: pd.DataFrame, table_name: str, engine) -> None:
    """ Load transformed data into the staging schema """

    truncate_staging_table(table_name, engine)

    df.to_sql(name=table_name, con=engine,schema="staging", if_exists="append", index=False, method="multi")

    logger.info("%s: Loaded %d row(s) into staging.", table_name, len(df),)


# ==========================================================
# Table Processing
# ==========================================================

def process_table(table_name: str, engine) -> None:
    """ Execute the complete ETL process for one table """

    logger.info("Processing table: %s", table_name)

    with engine.connect() as conn:
        df = pd.read_sql(text(f"SELECT * FROM raw.{table_name}"),conn,)

    df = TRANSFORMATIONS[table_name](df, engine)

    df = select_staging_columns(df, table_name,)
    
    load_to_staging(df, table_name, engine)


# ==========================================================
# Main
# ==========================================================

def main() -> None:
    """ Execute the Raw -> Staging ETL pipeline """

    logger.info("=" * 60)
    logger.info("Starting Raw -> Staging ETL")
    logger.info("=" * 60)

    engine = get_engine()

    successful = 0
    failed = 0

    try:
        
        for table_name in TRANSFORMATIONS:
            try:
                process_table(table_name, engine)
                successful += 1

            except Exception:
                failed += 1
                logger.exception("%s: ETL failed.", table_name,)
        
    finally:
        dispose_engine()

    logger.info("=" * 60)
    logger.info("Raw -> Staging ETL Complete")
    logger.info("Successful tables : %d", successful)
    logger.info("Failed tables     : %d", failed)
    logger.info("Invalid row(s)    : %d", INVALID_ROW_COUNT,)
    logger.info("=" * 60)

    if failed > 0:
        raise RuntimeError()

if __name__ == "__main__":
    main()
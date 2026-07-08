""" Warehouse ETL loader functions.

Responsibilities
----------------
- Truncate warehouse tables
- Load dimension tables
- Load fact tables
- Log ETL progress

The warehouse is populated from the staging schema using
set-based SQL operations. """

from sqlalchemy import text
from sqlalchemy.engine import Connection

from pipeline.logger import get_logger

logger = get_logger()

# =============================================================================
# SQL STATEMENTS
# =============================================================================

TRUNCATE_SQL = """
TRUNCATE TABLE

    warehouse.fact_delivery,
    warehouse.fact_render,
    warehouse.fact_timesheet,
    warehouse.fact_task_assignment,

    warehouse.dim_date,
    warehouse.dim_artist,
    warehouse.dim_task,
    warehouse.dim_shot,
    warehouse.dim_sequence,
    warehouse.dim_project

RESTART IDENTITY CASCADE;
"""


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def execute_sql(conn: Connection, query: str) -> None:
    """ Execute a SQL statement """

    conn.execute(text(query))


def execute_insert(conn: Connection, query: str, table_name: str) -> None:
    """ Execute an INSERT statement and log the number of rows inserted """

    logger.info(f"Starting load: {table_name}")

    result = conn.execute(text(query))

    logger.info(f"Completed load: {table_name}" f"({result.rowcount:,} rows inserted).")


def truncate_warehouse_tables(conn: Connection) -> None:
    """ Truncate all warehouse tables.

    Tables are truncated in reverse dependency order to
    respect foreign key relationships.

    Identity columns are reset to ensure deterministic
    surrogate keys across full refresh loads """

    logger.info("Truncating warehouse tables...")

    execute_sql(conn, TRUNCATE_SQL)

    logger.info("Warehouse tables truncated successfully.")


# =============================================================================
# DIMENSION LOAD SQL
# =============================================================================

DIM_PROJECT_SQL: str = """
INSERT INTO warehouse.dim_project
(
    project_id,
    project_name,
    project_type,
    client,
    budget_million_usd,
    complexity,
    start_date,
    end_date,
    status
)
SELECT
    project.project_id,
    project.project_name,
    project.project_type,
    project.client,
    project.budget_million_usd,
    project.complexity,
    project.start_date,
    project.end_date,
    project.status
FROM staging.projects AS project;
"""


DIM_SEQUENCE_SQL: str = """
INSERT INTO warehouse.dim_sequence
(
    sequence_id,
    project_key,
    sequence_name,
    complexity,
    start_date,
    end_date,
    status
)
SELECT
    sequence.sequence_id,
    dim_project.project_key,
    sequence.sequence_name,
    sequence.complexity,
    sequence.start_date,
    sequence.end_date,
    sequence.status
FROM staging.sequences AS sequence
JOIN warehouse.dim_project AS dim_project
    ON sequence.project_id = dim_project.project_id;
"""


DIM_SHOT_SQL: str = """
INSERT INTO warehouse.dim_shot
(
    shot_id,
    sequence_key,
    shot_name,
    complexity,
    frame_count,
    start_date,
    end_date,
    status
)
SELECT
    shot.shot_id,
    dim_sequence.sequence_key,
    shot.shot_name,
    shot.complexity,
    shot.frame_count,
    shot.start_date,
    shot.end_date,
    shot.status
FROM staging.shots AS shot
JOIN warehouse.dim_sequence AS dim_sequence
    ON shot.sequence_id = dim_sequence.sequence_id;
"""


DIM_TASK_SQL: str = """
INSERT INTO warehouse.dim_task
(
    task_id,
    shot_key,
    department,
    estimated_hours,
    priority,
    start_date,
    end_date,
    status
)
SELECT
    task.task_id,
    dim_shot.shot_key,
    task.department,
    task.estimated_hours,
    task.priority,
    task.start_date,
    task.end_date,
    task.status
FROM staging.tasks AS task
JOIN warehouse.dim_shot AS dim_shot
    ON task.shot_id = dim_shot.shot_id;
"""


DIM_ARTIST_SQL: str = """
INSERT INTO warehouse.dim_artist
(
    artist_id,
    artist_name,
    department,
    experience_years
)
SELECT
    artist.artist_id,
    artist.artist_name,
    artist.department,
    artist.experience_years
FROM staging.artists AS artist;
"""


DIM_DATE_SQL: str = """
INSERT INTO warehouse.dim_date
(
    full_date,
    day,
    month,
    month_name,
    quarter,
    year,
    week_of_year,
    day_of_week,
    weekday_name,
    is_weekend
)
SELECT
    date_dim.full_date,
    EXTRACT(DAY FROM date_dim.full_date)::INTEGER,
    EXTRACT(MONTH FROM date_dim.full_date)::INTEGER,
    TRIM(TO_CHAR(date_dim.full_date, 'Month')),
    EXTRACT(QUARTER FROM date_dim.full_date)::INTEGER,
    EXTRACT(YEAR FROM date_dim.full_date)::INTEGER,
    EXTRACT(WEEK FROM date_dim.full_date)::INTEGER,
    EXTRACT(ISODOW FROM date_dim.full_date)::INTEGER,
    TRIM(TO_CHAR(date_dim.full_date, 'Day')),
    EXTRACT(ISODOW FROM date_dim.full_date) IN (6, 7)
FROM
(
    SELECT DISTINCT full_date
    FROM
    (
        SELECT start_date AS full_date FROM staging.projects
        UNION ALL
        SELECT end_date FROM staging.projects

        UNION ALL
        SELECT start_date FROM staging.sequences
        UNION ALL
        SELECT end_date FROM staging.sequences

        UNION ALL
        SELECT start_date FROM staging.shots
        UNION ALL
        SELECT end_date FROM staging.shots

        UNION ALL
        SELECT start_date FROM staging.tasks
        UNION ALL
        SELECT end_date FROM staging.tasks

        UNION ALL
        SELECT assignment_date FROM staging.task_assignments

        UNION ALL
        SELECT work_date FROM staging.timesheets

        UNION ALL
        SELECT submission_date FROM staging.render_jobs
        UNION ALL
        SELECT completion_date FROM staging.render_jobs

        UNION ALL
        SELECT delivery_date FROM staging.deliveries
    ) AS dates
    WHERE full_date IS NOT NULL
) AS date_dim
ORDER BY date_dim.full_date;
"""

FACT_TASK_ASSIGNMENT_SQL: str = """
INSERT INTO warehouse.fact_task_assignment
(
    assignment_id,
    task_key,
    artist_key,
    assignment_date,
    assigned_hours
)
SELECT
    assignment.assignment_id,
    dim_task.task_key,
    dim_artist.artist_key,
    assignment.assignment_date,
    assignment.assigned_hours
FROM staging.task_assignments AS assignment
JOIN warehouse.dim_task AS dim_task
    ON assignment.task_id = dim_task.task_id
JOIN warehouse.dim_artist AS dim_artist
    ON assignment.artist_id = dim_artist.artist_id;
"""

FACT_TIMESHEET_SQL: str = """
INSERT INTO warehouse.fact_timesheet
(
    timesheet_id,
    assignment_key,
    work_date,
    hours_logged
)
SELECT
    timesheet.timesheet_id,
    fact_assignment.assignment_key,
    timesheet.work_date,
    timesheet.hours_logged
FROM staging.timesheets AS timesheet
JOIN warehouse.fact_task_assignment AS fact_assignment
    ON timesheet.assignment_id = fact_assignment.assignment_id;
"""

FACT_RENDER_SQL: str = """
INSERT INTO warehouse.fact_render
(
    render_id,
    shot_key,
    submission_date,
    completion_date,
    frame_count,
    render_engine,
    render_status,
    render_hours
)
SELECT
    render.render_id,
    dim_shot.shot_key,
    render.submission_date,
    render.completion_date,
    render.frame_count,
    render.render_engine,
    render.render_status,
    render.render_hours
FROM staging.render_jobs AS render
JOIN warehouse.dim_shot AS dim_shot
    ON render.shot_id = dim_shot.shot_id;
"""

FACT_DELIVERY_SQL: str = """
INSERT INTO warehouse.fact_delivery
(
    delivery_id,
    shot_key,
    delivery_date,
    version,
    client_status,
    review_days,
    final_delivery
)
SELECT
    delivery.delivery_id,
    dim_shot.shot_key,
    delivery.delivery_date,
    delivery.version,
    delivery.client_status,
    delivery.review_days,
    delivery.final_delivery
FROM staging.deliveries AS delivery
JOIN warehouse.dim_shot AS dim_shot
    ON delivery.shot_id = dim_shot.shot_id;
"""


# =============================================================================
# DIMENSION LOADERS
# =============================================================================

def load_dim_project(conn: Connection) -> None:
    """ Load the project dimension """

    execute_insert(conn, DIM_PROJECT_SQL, "warehouse.dim_project")


def load_dim_sequence(conn: Connection) -> None:
    """ Load the sequence dimension """

    execute_insert(conn, DIM_SEQUENCE_SQL, "warehouse.dim_sequence")


def load_dim_shot(conn: Connection) -> None:
    """ Load the shot dimension """

    execute_insert(conn, DIM_SHOT_SQL, "warehouse.dim_shot")


def load_dim_task(conn: Connection) -> None:
    """ Load the task dimension """

    execute_insert(conn, DIM_TASK_SQL, "warehouse.dim_task")


def load_dim_artist(conn: Connection) -> None:
    """ Load the artist dimension """

    execute_insert(conn, DIM_ARTIST_SQL, "warehouse.dim_artist")


def load_dim_date(conn: Connection) -> None:
    """ Load the date dimension """

    execute_insert(conn, DIM_DATE_SQL, "warehouse.dim_date")


# =============================================================================
# FACT LOADERS
# =============================================================================

def load_fact_task_assignment(conn: Connection) -> None:
    """ Load the task assignment fact table """

    execute_insert(conn, FACT_TASK_ASSIGNMENT_SQL, "warehouse.fact_task_assignment")


def load_fact_timesheet( conn: Connection) -> None:
    """ Load the timesheet fact table """

    execute_insert(conn, FACT_TIMESHEET_SQL, "warehouse.fact_timesheet")


def load_fact_render(conn: Connection) -> None:
    """ Load the render fact table """

    execute_insert(conn, FACT_RENDER_SQL, "warehouse.fact_render")


def load_fact_delivery(conn: Connection) -> None:
    """ Load the delivery fact table """

    execute_insert(conn, FACT_DELIVERY_SQL, "warehouse.fact_delivery")
    
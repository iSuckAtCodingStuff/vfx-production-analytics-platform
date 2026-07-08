-- ============================================================================
-- Warehouse Layer Schema
--
-- Purpose: Analytics-ready dimensional model.
-- Contains dimensions and fact tables with enforced 
-- primary keys and foreign key relationships.
-- ============================================================================

-- ============================================================================
-- CREATE WAREHOUSE SCHEMA
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS warehouse;

-- ============================================================================
-- PROJECT DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_project
(
    project_key INTEGER GENERATED ALWAYS AS IDENTITY,

    project_id VARCHAR(10) NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    project_type VARCHAR(100) NOT NULL,
    client VARCHAR(255) NOT NULL,
    budget_million_usd NUMERIC(10,2) NOT NULL,
    complexity VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_project
        PRIMARY KEY (project_key),

    CONSTRAINT uq_dim_project_project_id
        UNIQUE (project_id),

    CONSTRAINT chk_dim_project_budget
        CHECK (budget_million_usd >= 0),

    CONSTRAINT chk_dim_project_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE warehouse.dim_project
IS 'Project dimension containing one record per VFX project.';

COMMENT ON COLUMN warehouse.dim_project.project_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.dim_project.project_id
IS 'Business key from staging.';

-- ============================================================================
-- SEQUENCE DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_sequence
(
    sequence_key INTEGER GENERATED ALWAYS AS IDENTITY,

    sequence_id VARCHAR(10) NOT NULL,

    project_key INTEGER NOT NULL,

    sequence_name VARCHAR(255) NOT NULL,
    complexity VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_sequence
        PRIMARY KEY (sequence_key),

    CONSTRAINT uq_dim_sequence_sequence_id
        UNIQUE (sequence_id),

    CONSTRAINT fk_dim_sequence_project
        FOREIGN KEY (project_key)
        REFERENCES warehouse.dim_project(project_key)
        ON DELETE RESTRICT,

    CONSTRAINT chk_dim_sequence_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE warehouse.dim_sequence
IS 'Sequence dimension. Each sequence belongs to exactly one project.';

COMMENT ON COLUMN warehouse.dim_sequence.sequence_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.dim_sequence.sequence_id
IS 'Business key from staging.';

COMMENT ON COLUMN warehouse.dim_sequence.project_key
IS 'References dim_project.';

-- ============================================================================
-- SHOT DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_shot
(
    shot_key INTEGER GENERATED ALWAYS AS IDENTITY,

    shot_id VARCHAR(10) NOT NULL,

    sequence_key INTEGER NOT NULL,

    shot_name VARCHAR(255) NOT NULL,
    complexity VARCHAR(50) NOT NULL,
    frame_count INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_shot
        PRIMARY KEY (shot_key),

    CONSTRAINT uq_dim_shot_shot_id
        UNIQUE (shot_id),

    CONSTRAINT fk_dim_shot_sequence
        FOREIGN KEY (sequence_key)
        REFERENCES warehouse.dim_sequence(sequence_key)
        ON DELETE RESTRICT,

    CONSTRAINT chk_dim_shot_frame_count
        CHECK (frame_count > 0),

    CONSTRAINT chk_dim_shot_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE warehouse.dim_shot
IS 'Shot dimension. Each shot belongs to a sequence.';

COMMENT ON COLUMN warehouse.dim_shot.shot_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.dim_shot.shot_id
IS 'Business key from staging.';

COMMENT ON COLUMN warehouse.dim_shot.sequence_key
IS 'References dim_sequence.';


-- ============================================================================
-- TASK DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_task
(
    task_key INTEGER GENERATED ALWAYS AS IDENTITY,

    task_id VARCHAR(10) NOT NULL,

    shot_key INTEGER NOT NULL,

    department VARCHAR(100) NOT NULL,
    estimated_hours NUMERIC(10,2) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(50) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_task
        PRIMARY KEY (task_key),

    CONSTRAINT uq_dim_task_task_id
        UNIQUE (task_id),

    CONSTRAINT fk_dim_task_shot
        FOREIGN KEY (shot_key)
        REFERENCES warehouse.dim_shot(shot_key)
        ON DELETE RESTRICT,

    CONSTRAINT chk_dim_task_estimated_hours
        CHECK (estimated_hours > 0),

    CONSTRAINT chk_dim_task_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE warehouse.dim_task
IS 'Task dimension. Each task belongs to a shot.';

COMMENT ON COLUMN warehouse.dim_task.task_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.dim_task.task_id
IS 'Business key from staging.';

COMMENT ON COLUMN warehouse.dim_task.shot_key
IS 'References dim_shot.';


-- ============================================================================
-- ARTIST DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_artist
(
    artist_key INTEGER GENERATED ALWAYS AS IDENTITY,

    artist_id VARCHAR(10) NOT NULL,
    artist_name VARCHAR(255) NOT NULL,
    department VARCHAR(100) NOT NULL,
    experience_years INTEGER NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_artist
        PRIMARY KEY (artist_key),

    CONSTRAINT uq_dim_artist_artist_id
        UNIQUE (artist_id),

    CONSTRAINT chk_dim_artist_experience
        CHECK (experience_years >= 0)
);

COMMENT ON TABLE warehouse.dim_artist
IS 'Artist dimension. Contains one record per artist.';

COMMENT ON COLUMN warehouse.dim_artist.artist_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.dim_artist.artist_id
IS 'Business key from staging.';


-- ============================================================================
-- DATE DIMENSION
-- ============================================================================

CREATE TABLE warehouse.dim_date
(
    full_date DATE NOT NULL,

    day INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter INTEGER NOT NULL,
    year INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    day_of_week INTEGER NOT NULL,
    weekday_name VARCHAR(20) NOT NULL,
    is_weekend BOOLEAN NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_dim_date
        PRIMARY KEY (full_date),

    CONSTRAINT chk_dim_date_day
        CHECK (day BETWEEN 1 AND 31),

    CONSTRAINT chk_dim_date_month
        CHECK (month BETWEEN 1 AND 12),

    CONSTRAINT chk_dim_date_quarter
        CHECK (quarter BETWEEN 1 AND 4),

    CONSTRAINT chk_dim_date_week
        CHECK (week_of_year BETWEEN 1 AND 53),

    CONSTRAINT chk_dim_date_day_of_week
        CHECK (day_of_week BETWEEN 1 AND 7)
);

COMMENT ON TABLE warehouse.dim_date
IS 'Calendar dimension used for analytics and reporting.';

COMMENT ON COLUMN warehouse.dim_date.full_date
IS 'Natural key representing the calendar date.';


-- ============================================================================
-- TASK ASSIGNMENT FACT
-- ============================================================================

CREATE TABLE warehouse.fact_task_assignment
(
    assignment_key INTEGER GENERATED ALWAYS AS IDENTITY,

    assignment_id VARCHAR(10) NOT NULL,

    task_key INTEGER NOT NULL,
    artist_key INTEGER NOT NULL,

    assignment_date DATE NOT NULL,
    assigned_hours NUMERIC(10,2) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_fact_task_assignment
        PRIMARY KEY (assignment_key),

    CONSTRAINT uq_fact_task_assignment_assignment_id
        UNIQUE (assignment_id),

    CONSTRAINT fk_fact_assignment_task
        FOREIGN KEY (task_key)
        REFERENCES warehouse.dim_task(task_key)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_assignment_artist
        FOREIGN KEY (artist_key)
        REFERENCES warehouse.dim_artist(artist_key)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_assignment_date
        FOREIGN KEY (assignment_date)
        REFERENCES warehouse.dim_date(full_date)
        ON DELETE RESTRICT,

    CONSTRAINT chk_fact_assignment_hours
        CHECK (assigned_hours >= 0)
);

COMMENT ON TABLE warehouse.fact_task_assignment
IS 'Assignment fact. One row per task assignment event.';

COMMENT ON COLUMN warehouse.fact_task_assignment.assignment_key
IS 'Warehouse surrogate key.';

COMMENT ON COLUMN warehouse.fact_task_assignment.assignment_id
IS 'Business key from staging (degenerate dimension).';


-- ============================================================================
-- TIMESHEET FACT
-- ============================================================================

CREATE TABLE warehouse.fact_timesheet
(
    timesheet_key INTEGER GENERATED ALWAYS AS IDENTITY,

    timesheet_id VARCHAR(10) NOT NULL,

    assignment_key INTEGER NOT NULL,

    work_date DATE NOT NULL,

    hours_logged NUMERIC(10,2) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_fact_timesheet
        PRIMARY KEY (timesheet_key),

    CONSTRAINT uq_fact_timesheet_timesheet_id
        UNIQUE (timesheet_id),

    CONSTRAINT fk_fact_timesheet_assignment
        FOREIGN KEY (assignment_key)
        REFERENCES warehouse.fact_task_assignment(assignment_key)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_timesheet_date
        FOREIGN KEY (work_date)
        REFERENCES warehouse.dim_date(full_date)
        ON DELETE RESTRICT,

    CONSTRAINT chk_fact_timesheet_hours
        CHECK (hours_logged >= 0)
);

COMMENT ON TABLE warehouse.fact_timesheet
IS 'Timesheet fact. One row per assignment per work date.';

COMMENT ON COLUMN warehouse.fact_timesheet.timesheet_id
IS 'Business key from staging (degenerate dimension).';


-- ============================================================================
-- RENDER FACT
-- ============================================================================

CREATE TABLE warehouse.fact_render
(
    render_key INTEGER GENERATED ALWAYS AS IDENTITY,

    render_id VARCHAR(10) NOT NULL,

    shot_key INTEGER NOT NULL,

    submission_date DATE NOT NULL,
    completion_date DATE NOT NULL,

    frame_count INTEGER NOT NULL,
    render_engine VARCHAR(100) NOT NULL,
    render_status VARCHAR(50) NOT NULL,
    render_hours NUMERIC(10,2) NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_fact_render
        PRIMARY KEY (render_key),

    CONSTRAINT uq_fact_render_render_id
        UNIQUE (render_id),

    CONSTRAINT fk_fact_render_shot
        FOREIGN KEY (shot_key)
        REFERENCES warehouse.dim_shot(shot_key)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_render_submission_date
        FOREIGN KEY (submission_date)
        REFERENCES warehouse.dim_date(full_date)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_render_completion_date
        FOREIGN KEY (completion_date)
        REFERENCES warehouse.dim_date(full_date)
        ON DELETE RESTRICT,

    CONSTRAINT chk_fact_render_frame_count
        CHECK (frame_count > 0),

    CONSTRAINT chk_fact_render_hours
        CHECK (render_hours >= 0),

    CONSTRAINT chk_fact_render_dates
        CHECK (completion_date >= submission_date)
);

COMMENT ON TABLE warehouse.fact_render
IS 'Render fact. One row per completed render event.';

COMMENT ON COLUMN warehouse.fact_render.render_id
IS 'Business key from staging (degenerate dimension).';


-- ============================================================================
-- DELIVERY FACT
-- ============================================================================

CREATE TABLE warehouse.fact_delivery
(
    delivery_key INTEGER GENERATED ALWAYS AS IDENTITY,

    delivery_id VARCHAR(10) NOT NULL,

    shot_key INTEGER NOT NULL,

    delivery_date DATE NOT NULL,
    version VARCHAR(10) NOT NULL,
    client_status VARCHAR(50) NOT NULL,
    review_days INTEGER NOT NULL,
    final_delivery BOOLEAN NOT NULL,

    _created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    _updated_at TIMESTAMP,

    CONSTRAINT pk_fact_delivery
        PRIMARY KEY (delivery_key),

    CONSTRAINT uq_fact_delivery_delivery_id
        UNIQUE (delivery_id),

    CONSTRAINT fk_fact_delivery_shot
        FOREIGN KEY (shot_key)
        REFERENCES warehouse.dim_shot(shot_key)
        ON DELETE RESTRICT,

    CONSTRAINT fk_fact_delivery_date
        FOREIGN KEY (delivery_date)
        REFERENCES warehouse.dim_date(full_date)
        ON DELETE RESTRICT,

    CONSTRAINT chk_fact_delivery_review_days
        CHECK (review_days >= 0)
);

COMMENT ON TABLE warehouse.fact_delivery
IS 'Delivery fact. One row per shot version delivered to the client.';

COMMENT ON COLUMN warehouse.fact_delivery.delivery_id
IS 'Business key from staging (degenerate dimension).';

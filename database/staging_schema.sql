-- ============================================================
-- Staging Layer Schema
--
-- Purpose:
-- Cleaned and validated data prior to loading into the warehouse.
-- Data types are enforced.
-- Basic quality checks are applied.
-- No primary keys or foreign keys.
-- ============================================================

-- ============================================================
-- Create Staging Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS staging;

-- ============================================================
-- Artists
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.artists (
    artist_id           VARCHAR(15)  NOT NULL,
    artist_name         VARCHAR(100) NOT NULL,
    department          VARCHAR(50)  NOT NULL,
    experience_years    NUMERIC(4,1) NOT NULL CHECK (experience_years >= 0),
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Projects
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.projects (
    project_id            VARCHAR(15)  NOT NULL,
    project_name          VARCHAR(100) NOT NULL,
    project_type          VARCHAR(30)  NOT NULL,
    client                VARCHAR(100) NOT NULL,
    budget_million_usd    NUMERIC(10,2) NOT NULL CHECK (budget_million_usd >= 0),
    complexity            VARCHAR(20)  NOT NULL,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(20) NOT NULL,
    _loaded_at            TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Sequences
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.sequences (
    sequence_id         VARCHAR(20) NOT NULL,
    project_id          VARCHAR(15) NOT NULL,
    sequence_name       VARCHAR(100) NOT NULL,
    complexity          VARCHAR(20) NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE,
    status              VARCHAR(20) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Shots
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.shots (
    shot_id             VARCHAR(20) NOT NULL,
    sequence_id         VARCHAR(20) NOT NULL,
    shot_name           VARCHAR(100) NOT NULL,
    complexity          VARCHAR(20) NOT NULL,
    frame_count         INTEGER NOT NULL CHECK (frame_count > 0),
    start_date          DATE NOT NULL,
    end_date            DATE,
    status              VARCHAR(20) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Tasks
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.tasks (
    task_id             VARCHAR(20) NOT NULL,
    shot_id             VARCHAR(20) NOT NULL,
    department          VARCHAR(50) NOT NULL,
    estimated_hours     NUMERIC(10,2) NOT NULL CHECK (estimated_hours >= 0),
    priority            VARCHAR(20) NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE,
    status              VARCHAR(20) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Task Assignments
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.task_assignments (
    assignment_id       VARCHAR(20) NOT NULL,
    task_id             VARCHAR(20) NOT NULL,
    artist_id           VARCHAR(15) NOT NULL,
    assigned_hours      NUMERIC(10,2) NOT NULL CHECK (assigned_hours >= 0),
    assignment_date     DATE NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Timesheets
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.timesheets (
    timesheet_id        VARCHAR(20) NOT NULL,
    assignment_id       VARCHAR(20) NOT NULL,
    work_date           DATE NOT NULL,
    hours_logged        NUMERIC(10,2) NOT NULL CHECK (hours_logged >= 0),
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Render Jobs
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.render_jobs (
    render_id           VARCHAR(20) NOT NULL,
    shot_id             VARCHAR(20) NOT NULL,
    frame_count         INTEGER NOT NULL CHECK (frame_count > 0),
    render_engine       VARCHAR(50) NOT NULL,
    render_status       VARCHAR(20) NOT NULL,
    render_hours        NUMERIC(10,2) NOT NULL CHECK (render_hours >= 0),
    submission_date     DATE NOT NULL,
    completion_date     DATE,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Deliveries
-- ============================================================

CREATE TABLE IF NOT EXISTS staging.deliveries (
    delivery_id         VARCHAR(20) NOT NULL,
    shot_id             VARCHAR(20) NOT NULL,
    version             INTEGER NOT NULL CHECK (version > 0),
    delivery_date       DATE NOT NULL,
    client_status       VARCHAR(30) NOT NULL,
    review_days         NUMERIC(10,2) CHECK (review_days >= 0),
    final_delivery      BOOLEAN NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL DEFAULT NOW()
);
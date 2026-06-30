-- ============================================================
-- VFX Production Analytics Platform
-- Raw Layer Schema
--
-- Purpose:
-- Landing zone for source CSV files.
-- Stores data exactly as received from the source CSVs.
-- No constraints, relationships, or transformations.
--
-- Author: Jaydeep Das
-- ============================================================

-- ============================================================
-- Create Raw Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS raw;

-- ============================================================
-- Artists
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.artists (
    artist_id          TEXT,
    artist_name        TEXT,
    department         TEXT,
    experience_years   TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Projects
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.projects (
    project_id           TEXT,
    project_name         TEXT,
    project_type         TEXT,
    client               TEXT,
    budget_million_usd   TEXT,
    complexity           TEXT,
    start_date           TEXT,
    end_date             TEXT,
    status               TEXT,
    _loaded_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Sequences
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.sequences (
    sequence_id        TEXT,
    project_id         TEXT,
    sequence_name      TEXT,
    complexity         TEXT,
    start_date         TEXT,
    end_date           TEXT,
    status             TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Shots
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.shots (
    shot_id            TEXT,
    sequence_id        TEXT,
    shot_name          TEXT,
    complexity         TEXT,
    frame_count        TEXT,
    start_date         TEXT,
    end_date           TEXT,
    status             TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Tasks
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.tasks (
    task_id            TEXT,
    shot_id            TEXT,
    department         TEXT,
    estimated_hours    TEXT,
    priority           TEXT,
    start_date         TEXT,
    end_date           TEXT,
    status             TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Task Assignments
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.task_assignments (
    assignment_id      TEXT,
    task_id            TEXT,
    artist_id          TEXT,
    assigned_hours     TEXT,
    assignment_date    TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Timesheets
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.timesheets (
    timesheet_id       TEXT,
    assignment_id      TEXT,
    work_date          TEXT,
    hours_logged       TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Render Jobs
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.render_jobs (
    render_id          TEXT,
    shot_id            TEXT,
    frame_count        TEXT,
    render_engine      TEXT,
    render_status      TEXT,
    render_hours       TEXT,
    submission_date    TEXT,
    completion_date    TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- Deliveries
-- ============================================================

CREATE TABLE IF NOT EXISTS raw.deliveries (
    delivery_id        TEXT,
    shot_id            TEXT,
    version            TEXT,
    delivery_date      TEXT,
    client_status      TEXT,
    review_days        TEXT,
    final_delivery     TEXT,
    _loaded_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
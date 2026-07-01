-- ============================================================
-- Warehouse Layer Schema
--
-- Purpose: Analytics-ready dimensional model.
-- Contains dimensions and fact tables with enforced
-- primary keys and foreign key relationships.
-- ============================================================

-- ============================================================
-- Create Warehouse Schema
-- ============================================================

CREATE SCHEMA IF NOT EXISTS warehouse;

-- ============================================================
-- Dimension Tables
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.dim_project (
    project_id            VARCHAR(15) PRIMARY KEY,
    project_name          VARCHAR(100) NOT NULL,
    project_type          VARCHAR(30) NOT NULL,
    client                VARCHAR(100) NOT NULL,
    budget_million_usd    NUMERIC(10,2) NOT NULL,
    complexity            VARCHAR(20) NOT NULL,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(20) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS warehouse.dim_sequence (
    sequence_id           VARCHAR(20) PRIMARY KEY,
    project_id            VARCHAR(15) NOT NULL,
    sequence_name         VARCHAR(100) NOT NULL,
    complexity            VARCHAR(20) NOT NULL,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(20) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_sequence_project
        FOREIGN KEY (project_id)
        REFERENCES warehouse.dim_project(project_id)
);

CREATE TABLE IF NOT EXISTS warehouse.dim_shot (
    shot_id               VARCHAR(20) PRIMARY KEY,
    sequence_id           VARCHAR(20) NOT NULL,
    shot_name             VARCHAR(100) NOT NULL,
    complexity            VARCHAR(20) NOT NULL,
    frame_count           INTEGER NOT NULL,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(20) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_shot_sequence
        FOREIGN KEY (sequence_id)
        REFERENCES warehouse.dim_sequence(sequence_id)
);

CREATE TABLE IF NOT EXISTS warehouse.dim_artist (
    artist_id             VARCHAR(15) PRIMARY KEY,
    artist_name           VARCHAR(100) NOT NULL,
    department            VARCHAR(50) NOT NULL,
    experience_years      NUMERIC(4,1) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Fact Tables
-- ============================================================

CREATE TABLE IF NOT EXISTS warehouse.fact_task (
    task_id               VARCHAR(20) PRIMARY KEY,
    shot_id               VARCHAR(20) NOT NULL,
    department            VARCHAR(50) NOT NULL,
    estimated_hours       NUMERIC(10,2) NOT NULL,
    priority              VARCHAR(20) NOT NULL,
    start_date            DATE NOT NULL,
    end_date              DATE,
    status                VARCHAR(20) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_task_shot
        FOREIGN KEY (shot_id)
        REFERENCES warehouse.dim_shot(shot_id)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_task_assignment (
    assignment_id         VARCHAR(20) PRIMARY KEY,
    task_id               VARCHAR(20) NOT NULL,
    artist_id             VARCHAR(15) NOT NULL,
    assigned_hours        NUMERIC(10,2) NOT NULL,
    assignment_date       DATE NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_assignment_task
        FOREIGN KEY (task_id)
        REFERENCES warehouse.fact_task(task_id),

    CONSTRAINT fk_assignment_artist
        FOREIGN KEY (artist_id)
        REFERENCES warehouse.dim_artist(artist_id)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_timesheet (
    timesheet_id          VARCHAR(20) PRIMARY KEY,
    assignment_id         VARCHAR(20) NOT NULL,
    work_date             DATE NOT NULL,
    hours_logged          NUMERIC(10,2) NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_timesheet_assignment
        FOREIGN KEY (assignment_id)
        REFERENCES warehouse.fact_task_assignment(assignment_id)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_render_job (
    render_id             VARCHAR(20) PRIMARY KEY,
    shot_id               VARCHAR(20) NOT NULL,
    frame_count           INTEGER NOT NULL,
    render_engine         VARCHAR(50) NOT NULL,
    render_status         VARCHAR(20) NOT NULL,
    render_hours          NUMERIC(10,2) NOT NULL,
    submission_date       DATE NOT NULL,
    completion_date       DATE,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_render_shot
        FOREIGN KEY (shot_id)
        REFERENCES warehouse.dim_shot(shot_id)
);

CREATE TABLE IF NOT EXISTS warehouse.fact_delivery (
    delivery_id           VARCHAR(20) PRIMARY KEY,
    shot_id               VARCHAR(20) NOT NULL,
    version               INTEGER NOT NULL,
    delivery_date         DATE NOT NULL,
    client_status         VARCHAR(30) NOT NULL,
    review_days           NUMERIC(10,2),
    final_delivery        BOOLEAN NOT NULL,
    created_at            TIMESTAMP NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_delivery_shot
        FOREIGN KEY (shot_id)
        REFERENCES warehouse.dim_shot(shot_id)
);
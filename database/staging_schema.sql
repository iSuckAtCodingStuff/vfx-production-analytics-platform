/*
===========================================================
 VFX Production Analytics Platform
 Staging Schema

 Purpose:
 Cleaned, validated and lightly normalized data ready for
 loading into the analytical warehouse.
===========================================================
*/

CREATE SCHEMA IF NOT EXISTS staging;

SET search_path TO staging;

-----------------------------------------------------------
-- PROJECTS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS projects
(
    project_id          VARCHAR(10) PRIMARY KEY,
    project_name        VARCHAR(100) NOT NULL,
    project_type        VARCHAR(50) NOT NULL,
    client              VARCHAR(100) NOT NULL,
    budget_million_usd  NUMERIC(10,2) NOT NULL,
    complexity          VARCHAR(20) NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE NOT NULL,
    status              VARCHAR(30) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT chk_projects_id
        CHECK (project_id ~ '^P[0-9]+$'),

    CONSTRAINT chk_projects_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE projects IS
'Cleaned project master data imported from the raw layer.';

COMMENT ON COLUMN projects.project_id IS
'Business identifier for the project.';

COMMENT ON COLUMN projects.total_shots IS
'Expected number of shots in the project.';


-----------------------------------------------------------
-- SEQUENCES
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS sequences
(
    sequence_id     VARCHAR(10) PRIMARY KEY,
    project_id      VARCHAR(10) NOT NULL,
    sequence_name   VARCHAR(100) NOT NULL,
    complexity      VARCHAR(20) NOT NULL,
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    status          VARCHAR(30) NOT NULL,
    _loaded_at      TIMESTAMP NOT NULL,

    CONSTRAINT fk_sequences_project
        FOREIGN KEY (project_id)
        REFERENCES projects(project_id),

    CONSTRAINT chk_sequences_id
        CHECK (sequence_id ~ '^SQ[0-9]+$'),

    CONSTRAINT chk_sequences_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE sequences IS
'Validated production sequences belonging to projects.';

COMMENT ON COLUMN sequences.sequence_id IS
'Business identifier for the sequence.';

COMMENT ON COLUMN sequences.project_id IS
'Reference to the parent project.';


-----------------------------------------------------------
-- SHOTS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS shots
(
    shot_id         VARCHAR(10) PRIMARY KEY,
    sequence_id     VARCHAR(10) NOT NULL,
    shot_name       VARCHAR(100) NOT NULL,
    complexity      VARCHAR(20) NOT NULL,
    frame_count     INTEGER NOT NULL,
    start_date      DATE NOT NULL,
    end_date        DATE NOT NULL,
    status          VARCHAR(30) NOT NULL,
    _loaded_at      TIMESTAMP NOT NULL,

    CONSTRAINT fk_shots_sequence
        FOREIGN KEY (sequence_id)
        REFERENCES sequences(sequence_id),

    CONSTRAINT chk_shots_id
        CHECK (shot_id ~ '^SH[0-9]+$'),

    CONSTRAINT chk_shots_frame_count
        CHECK (frame_count >= 0),

    CONSTRAINT chk_shots_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE shots IS
'Validated shot-level production data with redundant project information removed.';

COMMENT ON COLUMN shots.shot_id IS
'Business identifier for the shot.';

COMMENT ON COLUMN shots.sequence_id IS
'Reference to the parent sequence.';

COMMENT ON COLUMN shots.frame_count IS
'Total number of frames in the shot.';


-----------------------------------------------------------
-- TASKS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS tasks
(
    task_id             VARCHAR(10) PRIMARY KEY,
    shot_id             VARCHAR(10) NOT NULL,
    department          VARCHAR(50) NOT NULL,
    estimated_hours     NUMERIC(10,2) NOT NULL,
    priority            VARCHAR(20) NOT NULL,
    start_date          DATE NOT NULL,
    end_date            DATE NOT NULL,
    status              VARCHAR(30) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT fk_tasks_shot
        FOREIGN KEY (shot_id)
        REFERENCES shots(shot_id),

    CONSTRAINT chk_tasks_id
        CHECK (task_id ~ '^T[0-9]+$'),

    CONSTRAINT chk_tasks_estimated_hours
        CHECK (estimated_hours >= 0),

    CONSTRAINT chk_tasks_dates
        CHECK (end_date >= start_date)
);

COMMENT ON TABLE tasks IS
'Validated production tasks with redundant project and sequence references removed.';

COMMENT ON COLUMN tasks.task_id IS
'Business identifier for the task.';

COMMENT ON COLUMN tasks.shot_id IS
'Reference to the parent shot.';

COMMENT ON COLUMN tasks.estimated_hours IS
'Estimated effort required to complete the task.';


-----------------------------------------------------------
-- ARTISTS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS artists
(
    artist_id           VARCHAR(10) PRIMARY KEY,
    artist_name         VARCHAR(100) NOT NULL,
    department          VARCHAR(50) NOT NULL,
    experience_years    INTEGER NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT chk_artists_id
        CHECK (artist_id ~ '^A[0-9]+$'),

    CONSTRAINT chk_artists_experience
        CHECK (experience_years >= 0)
);

COMMENT ON TABLE artists IS
'Master list of production artists.';

COMMENT ON COLUMN artists.artist_id IS
'Business identifier for the artist.';

COMMENT ON COLUMN artists.experience_years IS
'Total years of professional production experience.';


-----------------------------------------------------------
-- TASK ASSIGNMENTS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS task_assignments
(
    assignment_id       VARCHAR(10) PRIMARY KEY,
    task_id             VARCHAR(10) NOT NULL,
    artist_id           VARCHAR(10) NOT NULL,
    assigned_hours      NUMERIC(10,2) NOT NULL,
    assignment_date     DATE NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT fk_assignments_task
        FOREIGN KEY (task_id)
        REFERENCES tasks(task_id),

    CONSTRAINT fk_assignments_artist
        FOREIGN KEY (artist_id)
        REFERENCES artists(artist_id),

    CONSTRAINT chk_assignments_id
        CHECK (assignment_id ~ '^TA[0-9]+$'),

    CONSTRAINT chk_assignments_hours
        CHECK (assigned_hours >= 0)
);

COMMENT ON TABLE task_assignments IS
'Bridge table assigning artists to production tasks.';

COMMENT ON COLUMN task_assignments.assignment_id IS
'Business identifier for the assignment.';

COMMENT ON COLUMN task_assignments.task_id IS
'Reference to the assigned task.';

COMMENT ON COLUMN task_assignments.artist_id IS
'Reference to the assigned artist.';

COMMENT ON COLUMN task_assignments.assigned_hours IS
'Planned number of hours assigned to the artist.';


-----------------------------------------------------------
-- TIMESHEETS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS timesheets
(
    timesheet_id        VARCHAR(10) PRIMARY KEY,
    assignment_id       VARCHAR(10) NOT NULL,
    work_date           DATE NOT NULL,
    hours_logged        NUMERIC(10,2) NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT fk_timesheets_assignment
        FOREIGN KEY (assignment_id)
        REFERENCES task_assignments(assignment_id),

    CONSTRAINT chk_timesheets_id
        CHECK (timesheet_id ~ '^TS[0-9]+$'),

    CONSTRAINT chk_timesheets_hours
        CHECK (hours_logged >= 0)
);

COMMENT ON TABLE timesheets IS
'Validated artist timesheets with redundant artist reference removed.';

COMMENT ON COLUMN timesheets.timesheet_id IS
'Business identifier for the timesheet entry.';

COMMENT ON COLUMN timesheets.assignment_id IS
'Reference to the associated task assignment.';

COMMENT ON COLUMN timesheets.hours_logged IS
'Actual number of hours worked.';


-----------------------------------------------------------
-- RENDER JOBS
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS render_jobs
(
    render_id           VARCHAR(10) PRIMARY KEY,
    shot_id             VARCHAR(10) NOT NULL,
    frame_count         INTEGER NOT NULL,
    render_engine       VARCHAR(50) NOT NULL,
    render_status       VARCHAR(30) NOT NULL,
    render_hours        NUMERIC(10,2) NOT NULL,
    submission_date     DATE NOT NULL,
    completion_date     DATE NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT fk_render_jobs_shot
        FOREIGN KEY (shot_id)
        REFERENCES shots(shot_id),

    CONSTRAINT chk_render_jobs_id
        CHECK (render_id ~ '^R[0-9]+$'),

    CONSTRAINT chk_render_jobs_frame_count
        CHECK (frame_count >= 0),

    CONSTRAINT chk_render_jobs_hours
        CHECK (render_hours >= 0),

    CONSTRAINT chk_render_jobs_dates
        CHECK (completion_date >= submission_date)
);

COMMENT ON TABLE render_jobs IS
'Validated render job records with redundant project and sequence references removed.';

COMMENT ON COLUMN render_jobs.render_id IS
'Business identifier for the render job.';

COMMENT ON COLUMN render_jobs.shot_id IS
'Reference to the rendered shot.';

COMMENT ON COLUMN render_jobs.render_hours IS
'Total render farm hours consumed.';


-----------------------------------------------------------
-- DELIVERIES
-----------------------------------------------------------

CREATE TABLE IF NOT EXISTS deliveries
(
    delivery_id         VARCHAR(10) PRIMARY KEY,
    shot_id             VARCHAR(10) NOT NULL,
    version             VARCHAR(10) NOT NULL,
    delivery_date       DATE NOT NULL,
    client_status       VARCHAR(30) NOT NULL,
    review_days         INTEGER NOT NULL,
    final_delivery      BOOLEAN NOT NULL,
    _loaded_at          TIMESTAMP NOT NULL,

    CONSTRAINT fk_deliveries_shot
        FOREIGN KEY (shot_id)
        REFERENCES shots(shot_id),

    CONSTRAINT chk_deliveries_id
        CHECK (delivery_id ~ '^D[0-9]+$'),

    CONSTRAINT chk_deliveries_version
        CHECK (version ~ '^V[0-9]+$'),

    CONSTRAINT chk_deliveries_review_days
        CHECK (review_days >= 0)
);

COMMENT ON TABLE deliveries IS
'Validated client delivery records with redundant project and sequence references removed.';

COMMENT ON COLUMN deliveries.delivery_id IS
'Business identifier for the delivery.';

COMMENT ON COLUMN deliveries.shot_id IS
'Reference to the delivered shot.';

COMMENT ON COLUMN deliveries.version IS
'Version identifier supplied by the production tracking system (e.g. V001).';

COMMENT ON COLUMN deliveries.final_delivery IS
'Indicates whether this delivery is the final approved version.';
-- ============================================================
-- Warehouse Indexes
--
-- Purpose: Improve query performance for joins and analytics.
-- ============================================================

-- ============================================================
-- Dimension Hierarchy
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_dim_sequence_project
ON warehouse.dim_sequence(project_id);

CREATE INDEX IF NOT EXISTS idx_dim_shot_sequence
ON warehouse.dim_shot(sequence_id);

-- ============================================================
-- Task Fact Table
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_fact_task_shot
ON warehouse.fact_task(shot_id);

CREATE INDEX IF NOT EXISTS idx_fact_task_department
ON warehouse.fact_task(department);

CREATE INDEX IF NOT EXISTS idx_fact_task_status
ON warehouse.fact_task(status);

CREATE INDEX IF NOT EXISTS idx_fact_task_priority
ON warehouse.fact_task(priority);

-- ============================================================
-- Task Assignment
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_assignment_task
ON warehouse.fact_task_assignment(task_id);

CREATE INDEX IF NOT EXISTS idx_assignment_artist
ON warehouse.fact_task_assignment(artist_id);

CREATE INDEX IF NOT EXISTS idx_assignment_date
ON warehouse.fact_task_assignment(assignment_date);

-- ============================================================
-- Timesheets
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_timesheet_assignment
ON warehouse.fact_timesheet(assignment_id);

CREATE INDEX IF NOT EXISTS idx_timesheet_work_date
ON warehouse.fact_timesheet(work_date);

-- ============================================================
-- Render Jobs
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_render_shot
ON warehouse.fact_render_job(shot_id);

CREATE INDEX IF NOT EXISTS idx_render_status
ON warehouse.fact_render_job(render_status);

CREATE INDEX IF NOT EXISTS idx_render_engine
ON warehouse.fact_render_job(render_engine);

-- ============================================================
-- Deliveries
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_delivery_shot
ON warehouse.fact_delivery(shot_id);

CREATE INDEX IF NOT EXISTS idx_delivery_client_status
ON warehouse.fact_delivery(client_status);

CREATE INDEX IF NOT EXISTS idx_delivery_date
ON warehouse.fact_delivery(delivery_date);

-- ============================================================
-- Artists
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_artist_department
ON warehouse.dim_artist(department);

-- ============================================================
-- Projects
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_project_client
ON warehouse.dim_project(client);

CREATE INDEX IF NOT EXISTS idx_project_status
ON warehouse.dim_project(status);

CREATE INDEX IF NOT EXISTS idx_project_type
ON warehouse.dim_project(project_type);
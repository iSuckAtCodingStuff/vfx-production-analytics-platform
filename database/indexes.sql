/*
===============================================================================
Warehouse Indexes

Purpose: Improve query performance for joins, filtering and analytics.
===============================================================================
*/

-- ============================================================================
-- DIMENSION TABLE INDEXES
-- ============================================================================

-- Foreign Key Indexes

CREATE INDEX IF NOT EXISTS idx_dim_sequence_project_key
ON warehouse.dim_sequence (project_key);

CREATE INDEX IF NOT EXISTS idx_dim_shot_sequence_key
ON warehouse.dim_shot (sequence_key);

CREATE INDEX IF NOT EXISTS idx_dim_task_shot_key
ON warehouse.dim_task (shot_key);


-- Frequently Filtered Dimension Columns

CREATE INDEX IF NOT EXISTS idx_dim_project_status
ON warehouse.dim_project (status);

CREATE INDEX IF NOT EXISTS idx_dim_project_client
ON warehouse.dim_project (client);

CREATE INDEX IF NOT EXISTS idx_dim_project_type
ON warehouse.dim_project (project_type);

CREATE INDEX IF NOT EXISTS idx_dim_sequence_status
ON warehouse.dim_sequence (status);

CREATE INDEX IF NOT EXISTS idx_dim_shot_status
ON warehouse.dim_shot (status);

CREATE INDEX IF NOT EXISTS idx_dim_task_department
ON warehouse.dim_task (department);

CREATE INDEX IF NOT EXISTS idx_dim_task_status
ON warehouse.dim_task (status);

CREATE INDEX IF NOT EXISTS idx_dim_task_priority
ON warehouse.dim_task (priority);

CREATE INDEX IF NOT EXISTS idx_dim_artist_department
ON warehouse.dim_artist (department);


-- ============================================================================
-- FACT TABLE INDEXES
-- ============================================================================

-- --------------------------------------------------------------------------
-- fact_task_assignment
-- --------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_fact_assignment_task_key
ON warehouse.fact_task_assignment (task_key);

CREATE INDEX IF NOT EXISTS idx_fact_assignment_artist_key
ON warehouse.fact_task_assignment (artist_key);

CREATE INDEX IF NOT EXISTS idx_fact_assignment_date
ON warehouse.fact_task_assignment (assignment_date);


-- --------------------------------------------------------------------------
-- fact_timesheet
-- --------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_fact_timesheet_assignment_key
ON warehouse.fact_timesheet (assignment_key);

CREATE INDEX IF NOT EXISTS idx_fact_timesheet_work_date
ON warehouse.fact_timesheet (work_date);


-- --------------------------------------------------------------------------
-- fact_render
-- --------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_fact_render_shot_key
ON warehouse.fact_render (shot_key);

CREATE INDEX IF NOT EXISTS idx_fact_render_submission_date
ON warehouse.fact_render (submission_date);

CREATE INDEX IF NOT EXISTS idx_fact_render_completion_date
ON warehouse.fact_render (completion_date);

CREATE INDEX IF NOT EXISTS idx_fact_render_status
ON warehouse.fact_render (render_status);

CREATE INDEX IF NOT EXISTS idx_fact_render_engine
ON warehouse.fact_render (render_engine);


-- --------------------------------------------------------------------------
-- fact_delivery
-- --------------------------------------------------------------------------

CREATE INDEX IF NOT EXISTS idx_fact_delivery_shot_key
ON warehouse.fact_delivery (shot_key);

CREATE INDEX IF NOT EXISTS idx_fact_delivery_delivery_date
ON warehouse.fact_delivery (delivery_date);

CREATE INDEX IF NOT EXISTS idx_fact_delivery_client_status
ON warehouse.fact_delivery (client_status);

CREATE INDEX IF NOT EXISTS idx_fact_delivery_final_delivery
ON warehouse.fact_delivery (final_delivery);


-- ============================================================================
-- DATE DIMENSION INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_dim_date_year
ON warehouse.dim_date (year);

CREATE INDEX IF NOT EXISTS idx_dim_date_month
ON warehouse.dim_date (month);

CREATE INDEX IF NOT EXISTS idx_dim_date_quarter
ON warehouse.dim_date (quarter);

CREATE INDEX IF NOT EXISTS idx_dim_date_week
ON warehouse.dim_date (week_of_year);

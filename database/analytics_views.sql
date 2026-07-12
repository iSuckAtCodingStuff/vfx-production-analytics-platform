/*
===========================================================
View: v_dim_task_context

Description:
Provides a reusable dimensional context for analytics.

Grain:
One row per task.

Purpose: Eliminates repeated joins across the
dimensional hierarchy (Project → Sequence → Shot → Task).

This view intentionally contains ONLY dimension tables.

No fact tables are included to avoid fan-out and duplicated
aggregations in analytical queries
===========================================================
*/

CREATE OR REPLACE VIEW warehouse.v_dim_task_context AS
SELECT
    -- =====================================================
    -- Project
    -- =====================================================
    p.project_key,
    p.project_id,
    p.project_name,
    p.project_type,
    p.status as project_status,
    p.complexity as project_complexity,
    p.budget_million_usd,
    -- =====================================================
    -- Sequence
    -- =====================================================
    s.sequence_key,
    s.sequence_id,
    s.sequence_name,
    -- =====================================================
    -- Shot
    -- =====================================================
    sh.shot_key,
    sh.shot_id,
    sh.shot_name,
    sh.status as shot_status,
    sh.complexity as shot_complexity,
    -- =====================================================
    -- Task
    -- =====================================================
    t.task_key,
    t.task_id,
    t.department,
    t.status,
    t.start_date,
    t.end_date
FROM warehouse.dim_task t
JOIN warehouse.dim_shot sh
    ON t.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key;
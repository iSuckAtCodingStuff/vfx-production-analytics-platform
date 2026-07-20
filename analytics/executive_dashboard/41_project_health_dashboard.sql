/*
===========================================================
Report: Project Executive Summary
Module: Executive Dashboard

Description:
Provides a consolidated executive-level KPI summary for each
project.

Grain:
One row per project.

Design:
- Every CTE independently aggregates to project level.
- No joins between fact tables.
- Prevents fan-out.
===========================================================
*/

WITH project_metrics AS (
    SELECT
        project_key,
        project_name,
        project_type,
        status AS project_status,
        complexity AS project_complexity,
        budget_million_usd
    FROM warehouse.dim_project
),
sequence_metrics AS (
    SELECT
        project_key,
        COUNT(*) AS total_sequences
    FROM warehouse.dim_sequence
    GROUP BY project_key
),
shot_metrics AS (
    SELECT
        ds.project_key,
        COUNT(*) AS total_shots
    FROM warehouse.dim_shot sh
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
task_metrics AS (
    SELECT
        ds.project_key,
        COUNT(*) AS total_tasks,
        COUNT(*) FILTER ( WHERE t.status = 'Completed') AS completed_tasks
    FROM warehouse.dim_task t
    JOIN warehouse.dim_shot sh
        ON t.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
artist_metrics AS (
    SELECT
        ds.project_key,
        COUNT(DISTINCT fta.artist_key) AS assigned_artists
    FROM warehouse.fact_task_assignment fta
    JOIN warehouse.dim_task t
        ON fta.task_key = t.task_key
    JOIN warehouse.dim_shot sh
        ON t.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
timesheet_metrics AS (
    SELECT
        ds.project_key,
        ROUND(SUM(ft.hours_logged),2) AS total_hours_logged
    FROM warehouse.fact_timesheet ft
    JOIN warehouse.fact_task_assignment fta
        ON ft.assignment_key = fta.assignment_key
    JOIN warehouse.dim_task t
        ON fta.task_key = t.task_key
    JOIN warehouse.dim_shot sh
        ON t.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
render_metrics AS (
    SELECT
        ds.project_key,
        COUNT(*) AS total_render_jobs,
        ROUND(SUM(fr.render_hours),2) AS total_render_hours,
        COUNT(*) FILTER (WHERE fr.render_status = 'Success') AS successful_renders
    FROM warehouse.fact_render fr
    JOIN warehouse.dim_shot sh
        ON fr.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
delivery_metrics AS (
    SELECT
        ds.project_key,
        COUNT(*) AS total_deliveries,
        COUNT(*) FILTER (WHERE fd.client_status = 'Approved') AS approved_deliveries
    FROM warehouse.fact_delivery fd
    JOIN warehouse.dim_shot sh
        ON fd.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
)
SELECT
    pm.project_name,
    pm.project_status,
    pm.project_type,
    pm.project_complexity,
    pm.budget_million_usd,
    COALESCE(sm.total_sequences,0) AS total_sequences,
    COALESCE(shm.total_shots,0) AS total_shots,
    COALESCE(tm.total_tasks,0) AS total_tasks,
    COALESCE(tm.completed_tasks,0) AS completed_tasks,
    ROUND(COALESCE(tm.completed_tasks * 100.0 / NULLIF(tm.total_tasks,0), 0), 2) AS task_completion_pct,
    COALESCE(am.assigned_artists,0) AS assigned_artists,
    COALESCE(tsm.total_hours_logged,0) AS total_hours_logged,
    COALESCE(rm.total_render_jobs,0) AS total_render_jobs,
    COALESCE(rm.total_render_hours,0) AS total_render_hours,
    COALESCE(rm.successful_renders,0) AS successful_renders,
    ROUND(COALESCE(rm.successful_renders * 100.0 / NULLIF(rm.total_render_jobs,0), 0), 2) AS render_success_pct,
    COALESCE(dm.total_deliveries,0) AS total_deliveries,
    COALESCE(dm.approved_deliveries,0) AS approved_deliveries,
    ROUND(COALESCE(dm.approved_deliveries * 100.0 / NULLIF(dm.total_deliveries,0), 0), 2) AS delivery_approval_pct
FROM project_metrics pm
LEFT JOIN sequence_metrics sm
    ON pm.project_key = sm.project_key
LEFT JOIN shot_metrics shm
    ON pm.project_key = shm.project_key
LEFT JOIN task_metrics tm
    ON pm.project_key = tm.project_key
LEFT JOIN artist_metrics am
    ON pm.project_key = am.project_key
LEFT JOIN timesheet_metrics tsm
    ON pm.project_key = tsm.project_key
LEFT JOIN render_metrics rm
    ON pm.project_key = rm.project_key
LEFT JOIN delivery_metrics dm
    ON pm.project_key = dm.project_key
ORDER BY
    pm.project_name;
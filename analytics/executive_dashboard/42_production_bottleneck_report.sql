/*
===========================================================
Report: Production Bottleneck Report
Module: Executive Dashboard

Description: Identifies potential production bottlenecks 
for each project.

Grain: One row per project.

Design:
- Each fact is independently aggregated.
- No fact-to-fact joins.
- Highlights operational bottlenecks.
===========================================================
*/

WITH task_metrics AS (
    SELECT
        ds.project_key,
        COUNT(*) AS total_tasks,
        COUNT(*) FILTER (WHERE t.status = 'Completed') AS completed_tasks,
        COUNT(*) FILTER (WHERE t.status <> 'Completed') AS pending_tasks
    FROM warehouse.dim_task t
    JOIN warehouse.dim_shot sh
        ON t.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
),
timesheet_metrics AS (
    SELECT
        ds.project_key,
        ROUND(SUM(ft.hours_logged),2) AS total_hours,
        ROUND(AVG(ft.hours_logged),2) AS avg_hours_per_entry
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
        COUNT(*) FILTER (WHERE fr.render_status = 'Failed') AS failed_renders,
        ROUND(AVG(fr.render_hours),2) AS avg_render_hours
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
        COUNT(*) FILTER (WHERE fd.client_status <> 'Approved') AS pending_deliveries
    FROM warehouse.fact_delivery fd
    JOIN warehouse.dim_shot sh
        ON fd.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence ds
        ON sh.sequence_key = ds.sequence_key
    GROUP BY ds.project_key
)
SELECT
    p.project_name,
    p.status AS project_status,
    tm.total_tasks,
    tm.completed_tasks,
    tm.pending_tasks,
    ROUND(tm.completed_tasks * 100.0 / NULLIF(tm.total_tasks,0), 2) AS completion_pct,
    COALESCE(ts.total_hours,0) AS total_hours_logged,
    COALESCE(ts.avg_hours_per_entry,0) AS avg_hours_per_entry,
    COALESCE(rm.total_render_jobs,0) AS total_render_jobs,
    COALESCE(rm.failed_renders,0) AS failed_renders,
    ROUND(COALESCE(rm.failed_renders * 100.0 / NULLIF(rm.total_render_jobs,0), 0), 2) AS render_failure_pct,
    COALESCE(rm.avg_render_hours,0) AS avg_render_hours,
    COALESCE(dm.total_deliveries,0) AS total_deliveries,
    COALESCE(dm.pending_deliveries,0) AS pending_deliveries,
    CASE
        WHEN(tm.completed_tasks * 100.0 / NULLIF(tm.total_tasks,0)) < 60
        THEN 'Task Backlog'
        WHEN (rm.failed_renders * 100.0 / NULLIF(rm.total_render_jobs,0)) > 20
        THEN 'Rendering Issues'
        WHEN dm.pending_deliveries > 5
        THEN 'Delivery Delay'
        ELSE 'Healthy'
    END AS primary_bottleneck
FROM warehouse.dim_project p
LEFT JOIN task_metrics tm
ON p.project_key = tm.project_key
LEFT JOIN timesheet_metrics ts
ON p.project_key = ts.project_key
LEFT JOIN render_metrics rm
ON p.project_key = rm.project_key
LEFT JOIN delivery_metrics dm
ON p.project_key = dm.project_key
ORDER BY
    completion_pct,
    render_failure_pct DESC,
    pending_deliveries DESC;
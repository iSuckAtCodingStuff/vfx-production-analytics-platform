/*
=========================================================================================
Report: Project Resource Summary
Module: Project Metrics

Description: Provides a consolidated resource summary for each project.

Production Notes: Each fact table is aggregated independently to avoid
fan-out caused by joining multiple one-to-many tables.
=========================================================================================
*/

WITH sequence_metrics AS (
    SELECT
        project_key,
        COUNT(*) AS total_sequences
    FROM warehouse.dim_sequence
    GROUP BY project_key
),
shot_metrics AS (
    SELECT
        s.project_key,
        COUNT(*) AS total_shots
    FROM warehouse.dim_shot sh
    JOIN warehouse.dim_sequence s
        ON sh.sequence_key = s.sequence_key
    GROUP BY s.project_key
),
task_metrics AS (
    SELECT
        s.project_key,
        COUNT(DISTINCT t.task_key) AS total_tasks,
        COUNT(DISTINCT fta.artist_key) AS total_artists,
        COALESCE(SUM(ft.hours_logged),0) AS total_hours_logged
    FROM warehouse.dim_task t
    JOIN warehouse.dim_shot sh
        ON t.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence s
        ON sh.sequence_key = s.sequence_key
    LEFT JOIN warehouse.fact_task_assignment fta
        ON t.task_key = fta.task_key
    LEFT JOIN warehouse.fact_timesheet ft
        ON fta.assignment_key = ft.assignment_key
    GROUP BY s.project_key
),
render_metrics AS (
    SELECT
        s.project_key,
        COUNT(*) AS total_render_jobs,
        SUM(fr.render_hours) AS total_render_hours
    FROM warehouse.fact_render fr
    JOIN warehouse.dim_shot sh
        ON fr.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence s
        ON sh.sequence_key = s.sequence_key
    GROUP BY s.project_key
),
delivery_metrics AS (
    SELECT
        s.project_key,
        COUNT(*) AS total_deliveries
    FROM warehouse.fact_delivery fd
    JOIN warehouse.dim_shot sh
        ON fd.shot_key = sh.shot_key
    JOIN warehouse.dim_sequence s
        ON sh.sequence_key = s.sequence_key
    GROUP BY s.project_key
)
SELECT
    p.project_name,
    COALESCE(sm.total_sequences,0) AS total_sequences,
    COALESCE(shm.total_shots,0) AS total_shots,
    COALESCE(tm.total_tasks,0) AS total_tasks,
    COALESCE(tm.total_artists,0) AS total_artists,
    ROUND(COALESCE(tm.total_hours_logged,0),2) AS total_hours_logged,
    COALESCE(rm.total_render_jobs,0) AS total_render_jobs,
    ROUND(COALESCE(rm.total_render_hours,0),2) AS total_render_hours,
    COALESCE(dm.total_deliveries,0) AS total_deliveries
FROM warehouse.dim_project p
LEFT JOIN sequence_metrics sm
ON p.project_key = sm.project_key
LEFT JOIN shot_metrics shm
ON p.project_key = shm.project_key
LEFT JOIN task_metrics tm
ON p.project_key = tm.project_key
LEFT JOIN render_metrics rm
ON p.project_key = rm.project_key
LEFT JOIN delivery_metrics dm
ON p.project_key = dm.project_key
ORDER BY
    p.project_name;
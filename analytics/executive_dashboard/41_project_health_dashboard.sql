/*
=================================================================================
Report: Project Health Dashboard
Module: Executive Dashboard

Description: Summarizes overall project health by combining task,
timesheet, render and delivery metrics. 
=================================================================================
*/

WITH project_metrics AS (
SELECT
    p.project_key,
    p.project_name,
    COUNT(DISTINCT sh.shot_key) AS total_shots,
    COUNT(DISTINCT t.task_key) AS total_tasks,
    COUNT(DISTINCT t.task_key)
        FILTER (WHERE t.status='Completed')
        AS completed_tasks,
    ROUND(COALESCE(SUM(ft.hours_logged),0), 2) AS total_hours,
    ROUND(COALESCE(SUM(fr.render_hours),0), 2) AS render_hours,
    COUNT(DISTINCT fd.delivery_key) AS deliveries
FROM warehouse.dim_project p
LEFT JOIN warehouse.dim_sequence s
ON p.project_key=s.project_key
LEFT JOIN warehouse.dim_shot sh
ON s.sequence_key=sh.sequence_key
LEFT JOIN warehouse.dim_task t
ON sh.shot_key=t.shot_key
LEFT JOIN warehouse.fact_task_assignment fta
ON t.task_key=fta.task_key
LEFT JOIN warehouse.fact_timesheet ft
ON fta.assignment_key=ft.assignment_key
LEFT JOIN warehouse.fact_render fr
ON sh.shot_key=fr.shot_key
LEFT JOIN warehouse.fact_delivery fd
ON sh.shot_key=fd.shot_key
GROUP BY p.project_key, p.project_name
)
SELECT
    project_name,
    total_shots,
    total_tasks,
    completed_tasks,
    ROUND(completed_tasks*100.0/ NULLIF(total_tasks,0), 2) AS completion_percentage,
    total_hours,
    render_hours,
    deliveries
FROM project_metrics
ORDER BY
    completion_percentage DESC,
    total_hours DESC;
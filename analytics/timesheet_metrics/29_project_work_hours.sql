/*
===========================================================
Report: Project Work Hours
Module: Timesheet Metrics

Description: Displays total hours worked for each project.
===========================================================
*/

SELECT
    p.project_name,
    ROUND(SUM(ft.hours_logged), 2) AS total_hours_logged
FROM warehouse.fact_timesheet ft
JOIN warehouse.fact_task_assignment fta
    ON ft.assignment_key = fta.assignment_key
JOIN warehouse.dim_task t
    ON fta.task_key = t.task_key
JOIN warehouse.dim_shot sh
    ON t.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
GROUP BY
    p.project_name
ORDER BY
    total_hours_logged DESC;
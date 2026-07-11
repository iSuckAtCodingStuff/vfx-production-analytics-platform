/*
===========================================================
Report: Artist Productivity
===========================================================
*/

SELECT
    a.artist_name,
    COUNT(DISTINCT t.task_key) AS tasks_assigned,
    ROUND(SUM(ft.hours_logged), 2) AS total_hours_logged,
    ROUND(COUNT(DISTINCT t.task_key)::NUMERIC / NULLIF(SUM(ft.hours_logged), 0), 3) AS tasks_per_hour
FROM warehouse.dim_artist a
JOIN warehouse.fact_task_assignment fta
    ON a.artist_key = fta.artist_key
JOIN warehouse.dim_task t
    ON fta.task_key = t.task_key
JOIN warehouse.fact_timesheet ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    a.artist_name
ORDER BY
    tasks_per_hour DESC NULLS LAST;
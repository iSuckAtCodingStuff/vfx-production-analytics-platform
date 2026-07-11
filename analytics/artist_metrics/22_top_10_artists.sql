/*
===========================================================
Report: Top 10 Artists by Hours Worked
===========================================================
*/

SELECT
    a.artist_name,
    a.department,
    ROUND(SUM(ft.hours_logged), 2) AS total_hours_logged
FROM warehouse.dim_artist a
JOIN warehouse.fact_task_assignment fta
    ON a.artist_key = fta.artist_key
JOIN warehouse.fact_timesheet ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    a.artist_name,
    a.department
ORDER BY
    total_hours_logged DESC
LIMIT 10;
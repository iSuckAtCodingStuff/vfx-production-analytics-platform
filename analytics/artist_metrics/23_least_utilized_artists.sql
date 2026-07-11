/*
===========================================================
Report: Least Utilized Artists
===========================================================
*/

SELECT
    a.artist_name,
    a.department,
    COALESCE(ROUND(SUM(ft.hours_logged), 2), 0) AS total_hours_logged
FROM warehouse.dim_artist a
LEFT JOIN warehouse.fact_task_assignment fta
    ON a.artist_key = fta.artist_key
LEFT JOIN warehouse.fact_timesheet ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    a.artist_name,
    a.department
ORDER BY
    total_hours_logged ASC
LIMIT 10;
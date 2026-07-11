/*
===========================================================
Report: Department Utilization
Module: Artist Metrics

Description: Shows total hours contributed by each 
department.
===========================================================
*/

SELECT
    a.department,
    COUNT(DISTINCT a.artist_key) AS total_artists,
    ROUND(SUM(ft.hours_logged), 2) AS total_hours_logged,
    ROUND(AVG(ft.hours_logged), 2) AS average_hours_per_entry
FROM warehouse.dim_artist a
JOIN warehouse.fact_task_assignment fta
    ON a.artist_key = fta.artist_key
JOIN warehouse.fact_timesheet ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    a.department
ORDER BY
    total_hours_logged DESC;
/*
===========================================================
Report: Artist Workload
Module: Artist Metrics

Description: Displays total hours logged by each artist.
===========================================================
*/

SELECT
    a.artist_name,
    a.department,
    ROUND(COALESCE(SUM(ft.hours_logged), 0), 2) AS total_hours_logged
FROM warehouse.dim_artist AS a
LEFT JOIN warehouse.fact_task_assignment AS fta
    ON a.artist_key = fta.artist_key
LEFT JOIN warehouse.fact_timesheet AS ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    a.artist_name,
    a.department
ORDER BY
    total_hours_logged DESC;
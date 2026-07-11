/*
===========================================================
Report: Average Hours per Artist
===========================================================
*/

SELECT
    department,
    ROUND(AVG(total_hours), 2) AS average_hours_per_artist
FROM (
    SELECT
        a.artist_key,
        a.department,
        SUM(ft.hours_logged) AS total_hours
    FROM warehouse.dim_artist a
    JOIN warehouse.fact_task_assignment fta
        ON a.artist_key = fta.artist_key
    JOIN warehouse.fact_timesheet ft
        ON fta.assignment_key = ft.assignment_key
    GROUP BY
        a.artist_key,
        a.department
) artist_hours
GROUP BY
    department
ORDER BY
    average_hours_per_artist DESC;
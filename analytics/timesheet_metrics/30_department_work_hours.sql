/*
===================================================================
Report: Department Work Hours
Module: Timesheet Metrics

Description: Shows total work hours logged by each department.

===================================================================
*/

SELECT
    a.department,
    ROUND(SUM(ft.hours_logged), 2) AS total_hours_logged
FROM warehouse.fact_timesheet ft
JOIN warehouse.fact_task_assignment fta
    ON ft.assignment_key = fta.assignment_key
JOIN warehouse.dim_artist a
    ON fta.artist_key = a.artist_key
GROUP BY
    a.department
ORDER BY
    total_hours_logged DESC;
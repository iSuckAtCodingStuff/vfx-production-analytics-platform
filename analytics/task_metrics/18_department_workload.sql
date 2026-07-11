/*
===========================================================
Report: Department Workload
Module: Task Metrics

Description: Shows the workload distribution by 
department using both task count and total hours worked.
===========================================================
*/

SELECT
    t.department,
    COUNT(DISTINCT t.task_key) AS total_tasks,
    COUNT(DISTINCT fta.assignment_key) AS total_assignments,
    ROUND(COALESCE(SUM(ft.hours_logged), 0), 2) AS total_hours_logged
FROM warehouse.dim_task AS t
LEFT JOIN warehouse.fact_task_assignment AS fta
    ON t.task_key = fta.task_key
LEFT JOIN warehouse.fact_timesheet AS ft
    ON fta.assignment_key = ft.assignment_key
GROUP BY
    t.department
ORDER BY
    total_hours_logged DESC;
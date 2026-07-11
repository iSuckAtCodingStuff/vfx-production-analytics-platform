/*
===========================================================
Report: Tasks by Department
Module: Task Metrics

Description: Displays the number of tasks assigned to 
each department.
===========================================================
*/

SELECT
    department,
    COUNT(*) AS total_tasks
FROM warehouse.dim_task
GROUP BY
    department
ORDER BY
    total_tasks DESC;
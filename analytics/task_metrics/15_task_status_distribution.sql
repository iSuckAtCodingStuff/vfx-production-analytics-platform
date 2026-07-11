/*
===============================================================================
Report: Task Status Distribution
Module: Task Metrics

Description:
Shows the distribution of task statuses across the studio.
===============================================================================
*/

SELECT
    status,
    COUNT(*) AS total_tasks,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage_of_tasks
FROM warehouse.dim_task
GROUP BY
    status
ORDER BY
    total_tasks DESC;
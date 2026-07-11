/*
===========================================================
Report: Monthly Task Creation Trend
Module: Task Metrics

Description: Shows how many tasks were created each month.
===========================================================
*/

SELECT
    DATE_TRUNC('month', start_date)::DATE AS month,
    COUNT(*) AS tasks_created
FROM warehouse.dim_task
GROUP BY
    DATE_TRUNC('month', start_date)
ORDER BY
    month;
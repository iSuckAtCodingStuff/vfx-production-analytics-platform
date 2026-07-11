/*
=====================================================================
Report: Monthly Hours Trend
Module: Timesheet Metrics

Description: Displays the total production hours logged each month.
=====================================================================
*/

SELECT
    DATE_TRUNC('month', work_date)::DATE AS month,
    ROUND(SUM(hours_logged), 2) AS total_hours_logged
FROM warehouse.fact_timesheet
GROUP BY
    DATE_TRUNC('month', work_date)
ORDER BY
    month;
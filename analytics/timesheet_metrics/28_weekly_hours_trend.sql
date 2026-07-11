/*
===========================================================
Report: Weekly Hours Trend
Module: Timesheet Metrics

Description: Displays total hours logged each week.
===========================================================
*/

SELECT
    DATE_TRUNC('week', work_date)::DATE AS week_start,
    ROUND(SUM(hours_logged), 2) AS total_hours_logged
FROM warehouse.fact_timesheet
GROUP BY
    DATE_TRUNC('week', work_date)
ORDER BY
    week_start;
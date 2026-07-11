/*
==============================================================================
Report: Peak Production Weeks
Module: Timesheet Metrics

Description: Ranks production weeks based on total hours logged
==============================================================================
*/

WITH weekly_hours AS (
    SELECT
        DATE_TRUNC('week', work_date)::DATE AS week_start,
        SUM(hours_logged) AS total_hours_logged
    FROM warehouse.fact_timesheet
    GROUP BY
        DATE_TRUNC('week', work_date)
)
SELECT
    week_start,
    ROUND(total_hours_logged, 2) AS total_hours_logged,
    RANK() OVER (
        ORDER BY total_hours_logged DESC
    ) AS workload_rank
FROM weekly_hours
ORDER BY
    workload_rank,
    week_start;
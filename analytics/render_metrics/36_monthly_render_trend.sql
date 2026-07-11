/*
===========================================================
Report: Monthly Render Trend
===========================================================
*/

SELECT
    DATE_TRUNC('month', submission_date)::DATE AS month,
    COUNT(*) AS total_render_jobs,
    ROUND(SUM(render_hours), 2) AS total_render_hours
FROM warehouse.fact_render
GROUP BY DATE_TRUNC('month', submission_date)
ORDER BY
    month;
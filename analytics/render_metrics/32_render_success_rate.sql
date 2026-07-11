/*
===========================================================
Report: Render Success Rate
===========================================================
*/

SELECT
    render_status,
    COUNT(*) AS total_render_jobs,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM warehouse.fact_render
GROUP BY render_status
ORDER BY total_render_jobs DESC;
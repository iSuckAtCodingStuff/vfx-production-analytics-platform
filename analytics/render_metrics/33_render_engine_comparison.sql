/*
===========================================================
Report: Render Engine Comparison
===========================================================
*/

SELECT
    render_engine,
    COUNT(*) AS total_jobs,
    ROUND(SUM(render_hours), 2) AS total_render_hours,
    ROUND(AVG(render_hours), 2) AS average_render_hours
FROM warehouse.fact_render
GROUP BY
    render_engine
ORDER BY
    total_render_hours DESC;
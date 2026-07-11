/*
===========================================================
Report: Render Hours by Project
===========================================================
*/

SELECT
    p.project_name,
    COUNT(fr.render_key) AS total_render_jobs,
    ROUND(SUM(fr.render_hours), 2) AS total_render_hours
FROM warehouse.fact_render fr
JOIN warehouse.dim_shot sh
    ON fr.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
GROUP BY
    p.project_name
ORDER BY
    total_render_hours DESC;
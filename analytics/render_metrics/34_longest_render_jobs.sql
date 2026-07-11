/*
===========================================================
Report: Longest Render Jobs
===========================================================
*/

SELECT
    p.project_name,
    sh.shot_name,
    fr.render_engine,
    fr.render_hours,
    RANK() OVER (ORDER BY fr.render_hours DESC) AS render_rank
FROM warehouse.fact_render fr
JOIN warehouse.dim_shot sh
    ON fr.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
ORDER BY
    render_rank
LIMIT 10;
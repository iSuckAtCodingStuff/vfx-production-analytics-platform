/*
===========================================================
Report: Shots per Project
===========================================================
*/

SELECT
    p.project_name,
    COUNT(sh.shot_key) AS total_shots
FROM warehouse.dim_project p
JOIN warehouse.dim_sequence s
    ON p.project_key = s.project_key
JOIN warehouse.dim_shot sh
    ON s.sequence_key = sh.sequence_key
GROUP BY
    p.project_name
ORDER BY
    total_shots DESC;
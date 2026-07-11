/*
===========================================================
Report: Largest Sequences by Shot Count
===========================================================
*/

SELECT
    p.project_name,
    s.sequence_name,
    COUNT(sh.shot_key) AS total_shots
FROM warehouse.dim_sequence s
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
LEFT JOIN warehouse.dim_shot sh
    ON s.sequence_key = sh.sequence_key
GROUP BY
    p.project_name,
    s.sequence_name
ORDER BY
    total_shots DESC;
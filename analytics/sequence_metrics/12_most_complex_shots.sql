/*
===========================================================
Report: Most Complex Shots
===========================================================
*/

SELECT
    p.project_name,
    s.sequence_name,
    sh.shot_name,
    sh.complexity
FROM warehouse.dim_shot sh
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
ORDER BY
    sh.complexity DESC,
    p.project_name;
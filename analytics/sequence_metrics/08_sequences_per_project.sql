/*
===========================================================
Report: Sequences per Project
===========================================================
*/

SELECT
    p.project_name,
    COUNT(s.sequence_key) AS total_sequences
FROM warehouse.dim_project p
LEFT JOIN warehouse.dim_sequence s
    ON p.project_key = s.project_key
GROUP BY
    p.project_name
ORDER BY
    total_sequences DESC;
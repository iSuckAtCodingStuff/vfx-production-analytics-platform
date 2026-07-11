/*
===========================================================
Report: Shot Progress Report
===========================================================
*/

SELECT
    p.project_name,
    COUNT(*) AS total_shots,
    COUNT(*) FILTER (
        WHERE sh.status = 'Completed'
    ) AS completed_shots,
    ROUND(100.0 * COUNT(*) FILTER (
            WHERE sh.status = 'Completed'
        )/ COUNT(*), 2) AS completion_percentage
FROM warehouse.dim_project p
JOIN warehouse.dim_sequence s
    ON p.project_key = s.project_key
JOIN warehouse.dim_shot sh
    ON s.sequence_key = sh.sequence_key
GROUP BY
    p.project_name
ORDER BY
    completion_percentage DESC,
    p.project_name;
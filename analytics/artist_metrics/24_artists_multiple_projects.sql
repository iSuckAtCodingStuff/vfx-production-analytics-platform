/*
===========================================================
Report: Artists Working Across Multiple Projects
===========================================================
*/

SELECT
    a.artist_name,
    COUNT(DISTINCT p.project_key) AS total_projects
FROM warehouse.dim_artist a
JOIN warehouse.fact_task_assignment fta
    ON a.artist_key = fta.artist_key
JOIN warehouse.dim_task t
    ON fta.task_key = t.task_key
JOIN warehouse.dim_shot sh
    ON t.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
GROUP BY
    a.artist_name
HAVING
    COUNT(DISTINCT p.project_key) > 1
ORDER BY
    total_projects DESC,
    a.artist_name;
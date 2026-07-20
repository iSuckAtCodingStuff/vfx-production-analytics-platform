SELECT
    COUNT(DISTINCT artist_key)
FROM warehouse.fact_task_assignment;

SELECT
    project_name,
    COUNT(DISTINCT fta.artist_key) AS artists
FROM warehouse.dim_project p
JOIN warehouse.dim_sequence s
    ON p.project_key = s.project_key
JOIN warehouse.dim_shot sh
    ON s.sequence_key = sh.sequence_key
JOIN warehouse.dim_task t
    ON sh.shot_key = t.shot_key
JOIN warehouse.fact_task_assignment fta
    ON t.task_key = fta.task_key
GROUP BY project_name
ORDER BY project_name;
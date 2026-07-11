/*
===========================================================
Report: Tasks per Shot
Module: Task Metrics

Description: Displays the number of tasks associated 
with each shot.

===========================================================
*/

SELECT
    p.project_name,
    s.sequence_name,
    sh.shot_name,
    COUNT(t.task_key) AS total_tasks
FROM warehouse.dim_project AS p
JOIN warehouse.dim_sequence AS s
    ON p.project_key = s.project_key
JOIN warehouse.dim_shot AS sh
    ON s.sequence_key = sh.sequence_key
LEFT JOIN warehouse.dim_task AS t
    ON sh.shot_key = t.shot_key
GROUP BY
    p.project_name,
    s.sequence_name,
    sh.shot_name
ORDER BY
    total_tasks DESC,
    p.project_name;
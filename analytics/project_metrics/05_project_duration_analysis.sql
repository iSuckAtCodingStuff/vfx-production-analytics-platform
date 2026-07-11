/*
===========================================================
Report: Project Duration Analysis
Module: Project Metrics

Description: Calculates planned project duration.
===========================================================
*/

SELECT
    project_name,
    start_date,
    end_date,
    (end_date - start_date) AS duration_days
FROM warehouse.dim_project
ORDER BY duration_days DESC;
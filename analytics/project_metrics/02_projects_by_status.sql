/*
===========================================================
Report: Projects by Status
Module: Project Metrics

Description: Shows the number of projects in each 
production status.
===========================================================
*/

SELECT
    status,
    COUNT(*) AS total_projects
FROM warehouse.dim_project
GROUP BY status
ORDER BY total_projects DESC;
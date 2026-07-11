/*
===========================================================
Report: Project Complexity Analysis
Module: Project Metrics

Description: Shows the distribution of projects by 
complexity level.
===========================================================
*/

SELECT
    complexity,
    COUNT(*) AS total_projects,
    ROUND(AVG(budget_million_usd), 2) AS average_budget
FROM warehouse.dim_project
GROUP BY complexity
ORDER BY complexity;
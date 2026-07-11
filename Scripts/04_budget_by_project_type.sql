/*
===========================================================
Report: Budget by Project Type
Module: Project Metrics

Description: Summarizes project budgets grouped by 
project type.
===========================================================
*/

SELECT
    project_type,
    COUNT(*) AS total_projects,
    SUM(budget_million_usd) AS total_budget,
    ROUND(AVG(budget_million_usd), 2) AS average_budget
FROM warehouse.dim_project
GROUP BY project_type
ORDER BY total_budget DESC;
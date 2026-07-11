/*
===========================================================
Report: Project Overview
Module: Project Metrics

Description: Displays key information for every project, 
including status, type, budget, complexity, 
duration and start/end dates.
===========================================================
*/

SELECT
    project_id,
    project_name,
    project_type,
    status,
    complexity,
    budget_million_usd,
    start_date,
    end_date,
    (end_date - start_date) AS duration_days
FROM warehouse.dim_project
ORDER BY project_name;

-- Expected Output:
-- project_id
-- project_name
-- project_type
-- project_status
-- project_complexity
-- budget
-- start_date
-- end_date
-- duration_days
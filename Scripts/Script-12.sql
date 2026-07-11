SELECT DISTINCT status
FROM warehouse.dim_task
ORDER BY status;

SELECT DISTINCT status
FROM warehouse.dim_project
ORDER BY status;

SELECT DISTINCT status
FROM warehouse.dim_shot
ORDER BY status;

SELECT DISTINCT client_status
FROM warehouse.fact_delivery
ORDER BY client_status;
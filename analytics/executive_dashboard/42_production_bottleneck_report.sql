SELECT
    client_status,
    COUNT(*)
FROM warehouse.fact_delivery fd 
GROUP BY client_status ;
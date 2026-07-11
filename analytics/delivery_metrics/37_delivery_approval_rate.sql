/*
===============================================================================
Report: Delivery Approval Rate
Module: Delivery Metrics

Description: Displays the approval rate for deliveries by delivery status
===============================================================================
*/

SELECT
    client_status,
    COUNT(*) AS total_deliveries,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) AS percentage
FROM warehouse.fact_delivery
GROUP by client_status
ORDER by total_deliveries DESC;
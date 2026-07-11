/*
====================================================================================
Report: Average Review Time
Module: Delivery Metrics

Description: Calculates the average number of review days by delivery status.
====================================================================================
*/

SELECT
    client_status,
    ROUND(AVG(review_days), 2) AS average_review_days,
    MIN(review_days) AS minimum_review_days,
    MAX(review_days) AS maximum_review_days
FROM warehouse.fact_delivery
GROUP BY
    client_status
ORDER BY
    average_review_days;
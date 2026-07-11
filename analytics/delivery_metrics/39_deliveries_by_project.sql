/*
===========================================================
Report: Deliveries by Project
Module: Delivery Metrics

Description:
Shows the number of deliveries made for each project.
===========================================================
*/

SELECT
    p.project_name,
    COUNT(fd.delivery_key) AS total_deliveries,
    ROUND(AVG(fd.review_days), 2) AS average_review_days
FROM warehouse.fact_delivery fd
JOIN warehouse.dim_shot sh
    ON fd.shot_key = sh.shot_key
JOIN warehouse.dim_sequence s
    ON sh.sequence_key = s.sequence_key
JOIN warehouse.dim_project p
    ON s.project_key = p.project_key
GROUP BY
    p.project_name
ORDER BY
    total_deliveries DESC;
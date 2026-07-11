/*
===========================================================
Report: Shot Status Distribution
===========================================================
*/

SELECT
    status,
    COUNT(*) AS total_shots
FROM warehouse.dim_shot
GROUP BY
    status
ORDER BY
    total_shots DESC;
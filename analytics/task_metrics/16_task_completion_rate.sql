/*
======================================================================================================================
Report: Task Completion Rate
Module: Task Metrics

Description: Calculates overall task completion rate.

======================================================================================================================
*/

SELECT
    COUNT(*) AS total_tasks,
    COUNT(*) FILTER (WHERE status = 'Completed') AS completed_tasks,
    ROUND(COUNT(*) FILTER (WHERE status = 'Completed') * 100.0/ COUNT(*), 2) AS completion_percentage
FROM warehouse.dim_task;
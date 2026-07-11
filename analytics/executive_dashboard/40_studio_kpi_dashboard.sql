/*
===========================================================
Report: Studio KPI Dashboard
Module: Executive Dashboard

Description: High-level studio KPIs in a single-row 
executive summary.
===========================================================
*/

SELECT
    (SELECT COUNT(*) FROM warehouse.dim_project) AS total_projects,
    (SELECT COUNT(*) FROM warehouse.dim_artist) AS total_artists,
    (SELECT COUNT(*) FROM warehouse.dim_sequence) AS total_sequences,
    (SELECT COUNT(*) FROM warehouse.dim_shot) AS total_shots,
    (SELECT COUNT(*) FROM warehouse.dim_task) AS total_tasks,
    (SELECT ROUND(SUM(hours_logged),2) FROM warehouse.fact_timesheet) AS total_hours_logged,
    (SELECT ROUND(SUM(render_hours),2) FROM warehouse.fact_render) AS total_render_hours,
    (SELECT COUNT(*) FROM warehouse.fact_delivery) AS total_deliveries,
    (SELECT ROUND(COUNT(*) FILTER (WHERE client_status='Approved')*100.0/COUNT(*), 2) FROM warehouse.fact_delivery) AS approval_rate,
    (SELECT ROUND(COUNT(*) FILTER (WHERE render_status='Success')*100.0/COUNT(*), 2) FROM warehouse.fact_render) AS render_success_rate;
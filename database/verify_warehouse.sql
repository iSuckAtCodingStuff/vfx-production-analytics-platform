-- ============================================================================
-- ROW COUNT VALIDATION
-- ============================================================================

SELECT 'staging.projects' AS table_name, COUNT(*) AS row_count
FROM staging.projects

UNION ALL

SELECT 'warehouse.dim_project', COUNT(*)
FROM warehouse.dim_project

UNION ALL

SELECT 'staging.sequences', COUNT(*)
FROM staging.sequences

UNION ALL

SELECT 'warehouse.dim_sequence', COUNT(*)
FROM warehouse.dim_sequence

UNION ALL

SELECT 'staging.shots', COUNT(*)
FROM staging.shots

UNION ALL

SELECT 'warehouse.dim_shot', COUNT(*)
FROM warehouse.dim_shot

UNION ALL

SELECT 'staging.tasks', COUNT(*)
FROM staging.tasks

UNION ALL

SELECT 'warehouse.dim_task', COUNT(*)
FROM warehouse.dim_task

UNION ALL

SELECT 'staging.artists', COUNT(*)
FROM staging.artists

UNION ALL

SELECT 'warehouse.dim_artist', COUNT(*)
FROM warehouse.dim_artist

UNION ALL

SELECT 'warehouse.dim_date', COUNT(*)
FROM warehouse.dim_date

UNION ALL

SELECT 'staging.task_assignments', COUNT(*)
FROM staging.task_assignments

UNION ALL

SELECT 'warehouse.fact_task_assignment', COUNT(*)
FROM warehouse.fact_task_assignment

UNION ALL

SELECT 'staging.timesheets', COUNT(*)
FROM staging.timesheets

UNION ALL

SELECT 'warehouse.fact_timesheet', COUNT(*)
FROM warehouse.fact_timesheet

UNION ALL

SELECT 'staging.render_jobs', COUNT(*)
FROM staging.render_jobs

UNION ALL

SELECT 'warehouse.fact_render', COUNT(*)
FROM warehouse.fact_render

UNION ALL

SELECT 'staging.deliveries', COUNT(*)
FROM staging.deliveries

UNION ALL

SELECT 'warehouse.fact_delivery', COUNT(*)
FROM warehouse.fact_delivery

ORDER BY table_name;

-- ============================================================================
-- DUPLICATE BUSINESS IDs
-- ============================================================================

SELECT project_id, COUNT(*)
FROM warehouse.dim_project
GROUP BY project_id
HAVING COUNT(*) > 1;

SELECT sequence_id, COUNT(*)
FROM warehouse.dim_sequence
GROUP BY sequence_id
HAVING COUNT(*) > 1;

SELECT shot_id, COUNT(*)
FROM warehouse.dim_shot
GROUP BY shot_id
HAVING COUNT(*) > 1;

SELECT task_id, COUNT(*)
FROM warehouse.dim_task
GROUP BY task_id
HAVING COUNT(*) > 1;

SELECT artist_id, COUNT(*)
FROM warehouse.dim_artist
GROUP BY artist_id
HAVING COUNT(*) > 1;

SELECT assignment_id, COUNT(*)
FROM warehouse.fact_task_assignment
GROUP BY assignment_id
HAVING COUNT(*) > 1;

SELECT timesheet_id, COUNT(*)
FROM warehouse.fact_timesheet
GROUP BY timesheet_id
HAVING COUNT(*) > 1;

SELECT render_id, COUNT(*)
FROM warehouse.fact_render
GROUP BY render_id
HAVING COUNT(*) > 1;

SELECT delivery_id, COUNT(*)
FROM warehouse.fact_delivery
GROUP BY delivery_id
HAVING COUNT(*) > 1;

-- ============================================================================
-- FOREIGN KEY VALIDATION
-- ============================================================================

SELECT COUNT(*) AS invalid_sequence_project_keys
FROM warehouse.dim_sequence
WHERE project_key IS NULL;

SELECT COUNT(*) AS invalid_shot_sequence_keys
FROM warehouse.dim_shot
WHERE sequence_key IS NULL;

SELECT COUNT(*) AS invalid_task_shot_keys
FROM warehouse.dim_task
WHERE shot_key IS NULL;

SELECT COUNT(*) AS invalid_assignment_task_keys
FROM warehouse.fact_task_assignment
WHERE task_key IS NULL;

SELECT COUNT(*) AS invalid_assignment_artist_keys
FROM warehouse.fact_task_assignment
WHERE artist_key IS NULL;

SELECT COUNT(*) AS invalid_timesheet_assignment_keys
FROM warehouse.fact_timesheet
WHERE assignment_key IS NULL;

SELECT COUNT(*) AS invalid_render_shot_keys
FROM warehouse.fact_render
WHERE shot_key IS NULL;

SELECT COUNT(*) AS invalid_delivery_shot_keys
FROM warehouse.fact_delivery
WHERE shot_key IS NULL;

-- ============================================================================
-- DATE DIMENSION
-- ============================================================================

SELECT
    MIN(full_date) AS earliest_date,
    MAX(full_date) AS latest_date,
    COUNT(*) AS total_dates
FROM warehouse.dim_date;


-- ============================================================================
-- SAMPLE DIMENSIONS
-- ============================================================================

SELECT *
FROM warehouse.dim_project
LIMIT 5;

SELECT *
FROM warehouse.dim_sequence
LIMIT 5;

SELECT *
FROM warehouse.dim_shot
LIMIT 5;

SELECT *
FROM warehouse.dim_task
LIMIT 5;

SELECT *
FROM warehouse.dim_artist
LIMIT 5;

SELECT *
FROM warehouse.dim_date
LIMIT 5;


-- ============================================================================
-- SAMPLE FACTS
-- ============================================================================

SELECT *
FROM warehouse.fact_task_assignment
LIMIT 5;

SELECT *
FROM warehouse.fact_timesheet
LIMIT 5;

SELECT *
FROM warehouse.fact_render
LIMIT 5;

SELECT *
FROM warehouse.fact_delivery
LIMIT 5;

-- ============================================================================
-- END-TO-END VALIDATION
-- ============================================================================

SELECT
    p.project_name,
    s.sequence_name,
    sh.shot_name,
    t.department,
    a.artist_name,
    f.assigned_hours
FROM warehouse.fact_task_assignment AS f

JOIN warehouse.dim_task AS t
    ON f.task_key = t.task_key

JOIN warehouse.dim_shot AS sh
    ON t.shot_key = sh.shot_key

JOIN warehouse.dim_sequence AS s
    ON sh.sequence_key = s.sequence_key

JOIN warehouse.dim_project AS p
    ON s.project_key = p.project_key

JOIN warehouse.dim_artist AS a
    ON f.artist_key = a.artist_key

LIMIT 20;

-- ============================================================================
-- FULL REFRESH
-- ============================================================================

SELECT MIN(project_key), MAX(project_key)
FROM warehouse.dim_project;

SELECT MIN(sequence_key), MAX(sequence_key)
FROM warehouse.dim_sequence;

SELECT MIN(shot_key), MAX(shot_key)
FROM warehouse.dim_shot;

SELECT MIN(task_key), MAX(task_key)
FROM warehouse.dim_task;

SELECT MIN(artist_key), MAX(artist_key)
FROM warehouse.dim_artist;


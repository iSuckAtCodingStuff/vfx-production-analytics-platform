import pandas as pd
from logger import get_logger

# Logger
logger = get_logger(__name__)

# read csv files along with error handling
try:
    logger.info("Loading CSV files...")

    artists_df = pd.read_csv("./data/artists.csv")
    projects_df = pd.read_csv("./data/projects.csv")
    sequence_df = pd.read_csv("./data/sequence.csv")
    shots_df = pd.read_csv("./data/shots.csv")
    tasks_df = pd.read_csv("./data/tasks.csv")
    task_assign_df = pd.read_csv("./data/task_assignment.csv")
    timesheet_df = pd.read_csv("./data/timesheet.csv")
    render_jobs_df = pd.read_csv("./data/render_jobs.csv")
    deliveries_df = pd.read_csv("./data/deliveries.csv")
    logger.info("CSV files loaded successfully.")

except Exception:
    logger.exception("Failed while loading CSV files.")
    raise
<<<<<<< Updated upstream
=======

# Log data validation
logger.info("Running validation...")
>>>>>>> Stashed changes

# DATA VALIDATION

logger.info("Running validation...")

datasets = {
    "Artists": artists_df,
    "Projects": projects_df,
    "Sequences": sequence_df,
    "Shots": shots_df,
    "Tasks": tasks_df,
    "Task Assignments": task_assign_df,
    "Timesheets": timesheet_df,
    "Render Jobs": render_jobs_df,
    "Deliveries": deliveries_df
}

for name, df in datasets.items():
    print(f"{name}: {df.shape}")

for name, df in datasets.items():
    print(f"\n{name}")
    print(df.isnull().sum())

print(artists_df["artist_id"].duplicated().sum())

print(projects_df["project_id"].duplicated().sum())

print(sequence_df["sequence_id"].duplicated().sum())

print(shots_df["shot_id"].duplicated().sum())

invalid_sequences = (set(sequence_df["project_id"])- set(projects_df["project_id"]))

print(invalid_sequences)

invalid_shots = (set(shots_df["sequence_id"])- set(sequence_df["sequence_id"]))

print(invalid_shots)

invalid_tasks = (set(tasks_df["shot_id"])- set(shots_df["shot_id"]))

print(invalid_tasks)

invalid_artists = (set(task_assign_df["artist_id"])- set(artists_df["artist_id"]))

print(invalid_artists)

invalid_timesheets = (set(timesheet_df["assignment_id"])- set(task_assign_df["assignment_id"]))

print(invalid_timesheets)

invalid_deliveries = (set(deliveries_df["shot_id"])- set(shots_df["shot_id"]))

print(invalid_deliveries)

#Log data validation end
logger.info("Validation completed successfully.")

<<<<<<< Updated upstream

=======
# ------------------------------------
# Dataset Summary

logger.info(f"Artists: {artists_df.shape}")
logger.info(f"Projects: {projects_df.shape}")
logger.info(f"Sequences: {sequence_df.shape}")
logger.info(f"Shots: {shots_df.shape}")
logger.info(f"Tasks: {tasks_df.shape}")
logger.info(f"Task Assignments: {task_assign_df.shape}")


logger.info("Pipeline completed successfully.")
>>>>>>> Stashed changes

import pandas as pd

# read csv files for next step
artists_df = pd.read_csv("./data/artists.csv")
projects_df = pd.read_csv("./data/projects.csv")
sequence_df = pd.read_csv("./data/sequence.csv")
shots_df = pd.read_csv("./data/shots.csv")
tasks_df = pd.read_csv("./data/tasks.csv")
task_assign_df = pd.read_csv("./data/task_assignment.csv")
timesheet_df = pd.read_csv("./data/timesheet.csv")
render_jobs_df = pd.read_csv("./data/render_jobs.csv")
deliveries_df = pd.read_csv("./data/deliveries.csv")

# DATA VALIDATION

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

# Date logic validation for projects as well as sequence data

print((projects_df["start_date"] <= projects_df["end_date"]).all())

sequence_df.merge(projects_df[["project_id", "start_date", "end_date"]], on="project_id")

sequence_project_df = sequence_df.merge(projects_df[["project_id", "start_date", "end_date"]], on="project_id", suffixes=("_sequence", "_project"))

date_cols = [
    "start_date_sequence",
    "end_date_sequence",
    "start_date_project",
    "end_date_project"
]

for col in date_cols:
    sequence_project_df[col] = pd.to_datetime(sequence_project_df[col])

print((sequence_project_df["start_date_project"] <= sequence_project_df["start_date_sequence"]).all())

print((sequence_project_df["end_date_sequence"] <= sequence_project_df["end_date_project"]).all())

print(projects_df.columns.tolist())
print(sequence_df.columns.tolist())
print(shots_df.columns.tolist())
print(tasks_df.columns.tolist())
print(artists_df.columns.tolist())
print(task_assign_df.columns.tolist())
print(timesheet_df.columns.tolist())
print(render_jobs_df.columns.tolist())
print(deliveries_df.columns.tolist())

print(projects_df.shape)
print(sequence_df.shape)
print(shots_df.shape)
print(tasks_df.shape)
print(artists_df.shape)
print(task_assign_df.shape)
print(timesheet_df.shape)
print(render_jobs_df.shape)
print(deliveries_df.shape)

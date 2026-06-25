from artists import generate_artists
from projects import generate_projects
from sequence import generate_sequences
from shots import generate_shots
from tasks import generate_tasks
from task_assigment import generate_task_assignments
from timesheets import generate_timesheets
from render_jobs import generate_render_jobs
from deliveries import generate_deliveries

# department names and emp head counts dict for artist creation and dept count assignment
department_counts = {

    "Modeling":40,
    "Rigging":20,
    "Animation":60,
    "CFX":20,
    "FX":60,
    "Lighting":20,
    "Compositing":80

}

# generate projects using the below project names
project_names = [
    "Dragon Rider",
    "Bear in City",
    "Imaginary Bonds",
    "Galactic Guardians",
    "Sheep Quest",
    "Frozen History",
    "Teddy Bear",
    "Titan Rising",
    "Mystic Forest",
    "Solar Frontier"
]
# generate projects using below studio names
studio_names = [
    "Miller-Jones Entertainment",
    "Apex Studios",
    "Smith Media",
    "Positive Studios",
    "Quantum Entertainment",
    "Para-Mountain Entertainment",
    "Trixify Media House",
    "Blue Potato Entertainment",
    "Compass Media",
    "Story Store Studios"
]

artists_df = generate_artists(department_counts)

projects_df = generate_projects(project_names, studio_names)

sequence_df = generate_sequences(projects_df)

shots_df = generate_shots(sequence_df)

tasks_df = generate_tasks(shots_df)

task_assign_df = generate_task_assignments(tasks_df, artists_df)

timesheet_df = generate_timesheets(task_assign_df)

render_jobs_df = generate_render_jobs(shots_df)

deliveries_df = generate_deliveries(shots_df)

artists_df.to_csv("./data/artists.csv", index=False)
projects_df.to_csv("./data/projects.csv", index=False)
sequence_df.to_csv("./data/sequence.csv", index=False)
shots_df.to_csv("./data/shots.csv", index=False)
tasks_df.to_csv("./data/tasks.csv", index=False)
task_assign_df.to_csv("./data/task_assignment.csv", index=False)
timesheet_df.to_csv("./data/timesheet.csv", index=False)
render_jobs_df.to_csv("./data/render_jobs.csv", index=False)
deliveries_df.to_csv("./data/deliveries.csv", index=False)

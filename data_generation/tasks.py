import numpy as np
import pandas as pd
from datetime import timedelta
from utils import generate_id, get_status
#  Helper 1: Department per shot

def get_departments_for_shot(complexity):

    if complexity == "Low":

        options = [
            ["Lighting", "Compositing"],
            ["Animation", "Lighting", "Compositing"]
        ]

    elif complexity == "Medium":

        options = [
            ["Animation", "Lighting", "Compositing"],
            ["Animation", "FX", "Lighting", "Compositing"],
            ["Animation", "CFX", "Lighting", "Compositing"]
        ]

    else:

        return [
            "Modeling",
            "Rigging",
            "Animation",
            "CFX",
            "FX",
            "Lighting",
            "Compositing"
        ]

    return options[np.random.randint(len(options))]

# Helper 2: Estimated task completion hours

def generate_estimated_hours(complexity, frame_count):
    
    if complexity == "Low":

        return np.random.randint(5, 20)

    elif complexity == "Medium":

        return np.random.randint(20, 60)

    return np.random.randint(60, 200)

# helper 3: task priority 
def generate_priority(complexity):

    if complexity == "High":

        return np.random.choice(
            ["Medium", "High"],
            p=[0.3, 0.7]
        )

    elif complexity == "Medium":

        return np.random.choice(
            ["Low", "Medium", "High"],
            p=[0.2, 0.6, 0.2]
        )

    return np.random.choice(
        ["Low", "Medium"],
        p=[0.7, 0.3]
    )

# helper 4: task dates

def generate_task_dates(shot_start, shot_end):

    shot_duration = (shot_end - shot_start).days

    start_offset = np.random.randint(0, max(1, shot_duration // 2))

    task_start = (shot_start + timedelta(days=start_offset))

    remaining_days = (shot_end - task_start).days

    duration = np.random.randint(1, max(2, remaining_days + 1))

    task_end = (task_start + timedelta(days=duration))

    if task_end > shot_end:
        task_end = shot_end

    return task_start, task_end

# main generator task

def generate_tasks(shots_df):

    tasks = []

    task_num = 1

    for _, shot in shots_df.iterrows():

        shot_id = shot["shot_id"]

        project_id = shot["project_id"]

        sequence_id = shot["sequence_id"]

        shot_complexity = shot["complexity"]

        frame_count = shot["frame_count"]

        shot_start = pd.to_datetime(shot["start_date"]).date()

        shot_end = pd.to_datetime(shot["end_date"]).date()

        departments = (get_departments_for_shot(shot_complexity))

        for department in departments:

            task_start, task_end = (generate_task_dates(shot_start, shot_end))

            tasks.append({

                "task_id": generate_id("T", task_num),

                "project_id": project_id,

                "sequence_id": sequence_id,

                "shot_id": shot_id,

                "department": department,

                "estimated_hours": generate_estimated_hours(shot_complexity, frame_count),

                "priority": generate_priority(shot_complexity),

                "start_date": task_start,

                "end_date": task_end,

                "status": get_status(task_end)
            })

            task_num += 1

    return pd.DataFrame(tasks)
import numpy as np
import pandas as pd
from datetime import timedelta

from utils import generate_id


def generate_render_engine():

    return np.random.choice(
        ["Arnold", "V-Ray", "RenderMan"],
        p=[0.6, 0.25, 0.15]
    )


def generate_render_status():

    return np.random.choice(
        ["Success", "Failed"],
        p=[0.9, 0.1]
    )


def generate_render_hours(frame_count, complexity):

    if complexity == "Low":
        multiplier = np.random.uniform(0.02, 0.05)

    elif complexity == "Medium":
        multiplier = np.random.uniform(0.05, 0.10)

    else:
        multiplier = np.random.uniform(0.10, 0.25)

    return round(frame_count * multiplier, 2)


def generate_render_jobs(shots_df):

    render_jobs = []

    render_num = 1
    
    today = pd.Timestamp.today().date()

    for _, shot in shots_df.iterrows():

        if shot["status"] != "Completed":
            continue

        shot_id = shot["shot_id"]

        project_id = shot["project_id"]

        sequence_id = shot["sequence_id"]

        frame_count = shot["frame_count"]

        complexity = shot["complexity"]

        start_date = pd.to_datetime(shot["start_date"]).date()

        render_count = np.random.randint(1, 4)

        for _ in range(render_count):

            submission_date = (start_date + timedelta(days=np.random.randint(0, 15)))

            render_hours = (generate_render_hours(frame_count, complexity))

            completion_date = (submission_date + timedelta(hours=max(1, int(render_hours))))

            render_jobs.append({

                "render_id": generate_id("R", render_num),

                "project_id": project_id,

                "sequence_id": sequence_id,

                "shot_id": shot_id,

                "frame_count": frame_count,

                "render_engine": generate_render_engine(),

                "render_status": generate_render_status(),

                "render_hours": render_hours,

                "submission_date": submission_date,

                "completion_date": completion_date

            })

            render_num += 1

    return pd.DataFrame(render_jobs)
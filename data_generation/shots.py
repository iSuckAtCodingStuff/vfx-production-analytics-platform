# Import required libraries

import numpy as np
import pandas as pd
from datetime import timedelta

from utils import (generate_id, get_status)


def get_shot_count(sequence_complexity):
    """
    Determine number of shots
    based on sequence complexity.
    """

    if sequence_complexity == "Low":
        return np.random.randint(5, 15)

    elif sequence_complexity == "Medium":
        return np.random.randint(15, 40)

    return np.random.randint(40, 100)


def generate_shot_complexity():
    """
    Generate shot complexity.
    """

    return np.random.choice(
        ["Low", "Medium", "High"],
        p=[0.4, 0.4, 0.2]
    )


def generate_frame_count(complexity):
    """
    Generate frame counts based
    on shot complexity.
    """

    if complexity == "Low":
        return np.random.randint(40, 120)

    elif complexity == "Medium":
        return np.random.randint(120, 300)

    return np.random.randint(300, 1000)


def generate_shot_dates(sequence_start,sequence_end):
    """
    Generate shot dates within
    sequence boundaries.
    """

    sequence_duration = (sequence_end - sequence_start).days

    start_offset = np.random.randint(0, max(1, sequence_duration // 2))

    shot_start = (sequence_start + timedelta(days=start_offset))

    remaining_days = (sequence_end - shot_start).days

    duration = np.random.randint(5, max(6, remaining_days + 1))

    shot_end = (shot_start + timedelta(days=duration))

    if shot_end > sequence_end:
        shot_end = sequence_end

    return shot_start, shot_end


def generate_shots(sequences_df):

    shots = []

    shot_num = 1

    for _, sequence in sequences_df.iterrows():

        sequence_id = sequence["sequence_id"]

        project_id = sequence["project_id"]

        sequence_name = sequence["sequence_name"]

        sequence_complexity = sequence["complexity"]

        sequence_start = pd.to_datetime(sequence["start_date"]).date()

        sequence_end = pd.to_datetime(sequence["end_date"]).date()

        shot_count = get_shot_count(sequence_complexity)

        sequence_shot_num = 10

        for _ in range(shot_count):

            complexity = (generate_shot_complexity())

            frame_count = (generate_frame_count(complexity))

            shot_start, shot_end = (generate_shot_dates(sequence_start,sequence_end))

            shots.append({
                "shot_id": generate_id("SH", shot_num),

                "project_id": project_id,

                "sequence_id": sequence_id,

                "shot_name":(f"{sequence_name}"f"_SH"f"{sequence_shot_num:03}"),

                "complexity": complexity,

                "frame_count": frame_count,

                "start_date": shot_start,

                "end_date": shot_end,

                "status": get_status(shot_end)
            })

            shot_num += 1
            sequence_shot_num += 10

    return pd.DataFrame(shots)
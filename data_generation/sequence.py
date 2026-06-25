# Import required libraries

import numpy as np
import pandas as pd
from datetime import timedelta

from utils import (generate_id, get_status)


def get_sequence_count(budget):
    """
    Determine number of sequences based on project budget.
    Larger projects generally contain more sequences.
    """

    if budget < 50:
        return np.random.randint(5, 10)

    elif budget < 150:
        return np.random.randint(10, 18)

    return np.random.randint(18, 30)


def generate_sequence_complexity():
    """
    Generate sequence complexity.
    """

    return np.random.choice(
        ["Low", "Medium", "High"],
        p=[0.3, 0.5, 0.2]
    )


def generate_sequence_dates(project_start, project_end):
    """
    Generate sequence dates constrained within
    project start and end dates.
    """

    project_duration = (project_end - project_start).days

    start_offset = np.random.randint(0, max(1, project_duration // 2))

    sequence_start = (project_start + timedelta(days=start_offset))

    remaining_days = (project_end - sequence_start).days

    duration = np.random.randint(15, max(16, remaining_days + 1))

    sequence_end = (sequence_start + timedelta(days=duration))

    if sequence_end > project_end:
        sequence_end = project_end

    return sequence_start, sequence_end


def generate_sequences(projects_df):

    sequences = []

    sequence_num = 1

    for _, project in projects_df.iterrows():

        project_id = project["project_id"]

        project_sequence_num = 10

        project_budget = project["budget_million_usd"]

        project_start = pd.to_datetime(project["start_date"]).date()

        project_end = pd.to_datetime(project["end_date"]).date()

        sequence_count = get_sequence_count(project_budget)

        for seq_num in range(sequence_count):

            sequence_start, sequence_end = (generate_sequence_dates(project_start,project_end))
            
            complexity = (generate_sequence_complexity())

            sequences.append({

                "sequence_id":generate_id("SQ",sequence_num),
                "project_id": project_id,
                "sequence_name": f"{project_id}_SEQ{project_sequence_num:03}",
                "complexity": complexity,
                "start_date": sequence_start,
                "end_date": sequence_end,
                "status": get_status(sequence_end)
            })
            
            sequence_num += 1
            project_sequence_num += 10

    return pd.DataFrame(sequences)
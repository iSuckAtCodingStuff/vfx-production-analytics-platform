# Import required libraries

import numpy as np
import pandas as pd

from utils import generate_id


def get_artist_count(estimated_hours):
    """
    Determine how many artists should be assigned
    based on task effort.
    """

    if estimated_hours < 40:
        return 1

    elif estimated_hours < 100:
        return np.random.randint(1, 3)

    return np.random.randint(2, 5)


def generate_task_assignments(tasks_df, artists_df):

    assignments = []

    assignment_num = 1

    for _, task in tasks_df.iterrows():

        task_id = task["task_id"]

        department = task["department"]

        estimated_hours = task["estimated_hours"]

        assignment_date = task["start_date"]

        # Get artists belonging to the task department

        eligible_artists = artists_df[artists_df["department"] == department]

        if eligible_artists.empty:
            continue

        artist_count = get_artist_count(estimated_hours)

        assigned_artists = eligible_artists.sample(
            n=min(artist_count,len(eligible_artists)),replace=False
        )

        # Split estimated hours across artists

        weights = np.random.dirichlet(np.ones(len(assigned_artists)))

        assigned_hours = (weights * estimated_hours)

        for artist, hours in zip(
            assigned_artists.itertuples(), assigned_hours
        ):

            assignments.append({

                "assignment_id": generate_id("TA", assignment_num),

                "task_id": task_id,

                "artist_id": artist.artist_id,

                "assigned_hours": round(hours, 2),

                "assignment_date": assignment_date
            })

            assignment_num += 1

    return pd.DataFrame(assignments)
# Import required libraries

import numpy as np
import pandas as pd
from datetime import timedelta

from utils import generate_id


def get_next_workday(current_date):
    """
    Skip weekends.
    """

    next_date = current_date + timedelta(days=1)

    while next_date.weekday() >= 5:
        next_date += timedelta(days=1)

    return next_date


def generate_timesheets(task_assignments_df):

    timesheets = []

    timesheet_num = 1

    for _, assignment in task_assignments_df.iterrows():

        assignment_id = assignment["assignment_id"]

        artist_id = assignment["artist_id"]

        assigned_hours = assignment["assigned_hours"]

        start_date = pd.to_datetime(assignment["assignment_date"]).date()
        
        actual_hours = (assigned_hours * np.random.uniform(0.85, 1.20))

        remaining_hours = round(actual_hours, 2)

        work_date = start_date

        while remaining_hours > 0:

            daily_hours = round(np.random.uniform(4, 8), 2)

            if daily_hours > remaining_hours:
                daily_hours = remaining_hours

            timesheets.append({

                "timesheet_id":
                    generate_id("TS", timesheet_num),

                "assignment_id": assignment_id,

                "artist_id": artist_id,

                "work_date": work_date,

                "hours_logged": round(daily_hours, 2)

            })

            remaining_hours = round(remaining_hours - daily_hours, 2)

            work_date = get_next_workday(work_date)

            timesheet_num += 1

    return pd.DataFrame(timesheets)
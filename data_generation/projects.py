import numpy as np
import pandas as pd
from datetime import timedelta

from utils import (
    fake,
    generate_id,
    generate_showType_budget,
    get_status
)

# to seggregate shows as per complexicity
def generate_complexity():

    return np.random.choice(
        [
            "Low",
            "Medium",
            "High"
        ],
        p=[0.3, 0.4, 0.3]
    )

def generate_projects(project_names, studio_names):

    projects = []
    shuffled_studios = np.random.permutation(studio_names)

    for i, project_name in enumerate(project_names, start=1):

        project_type = np.random.choice(["Feature Film", "Streaming Series"], p=[0.6, 0.4])

        details = generate_showType_budget(project_type)
        complexity = generate_complexity()

        if complexity == "High":
            details["budget"]= np.random.randint(180, 250)
        else:
            details["budget"] = np.random.randint(15, 80)
            

        start_date = fake.date_between(
            start_date="-3y",
            end_date="today"
        )

        end_date = (start_date + timedelta( days=details["duration_days"]))

        projects.append({
            "project_id": generate_id("P", i),
            "project_name": project_name,
            "project_type": project_type,
            "client": shuffled_studios[i - 1],
            "budget_million_usd": details["budget"],
            "complexity": complexity,
            "start_date": start_date,
            "end_date": end_date,
            "status": get_status(end_date)
        })

    return pd.DataFrame(projects)
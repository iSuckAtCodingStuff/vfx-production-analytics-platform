# common imports

import numpy as np
import pandas as pd
from faker import Faker
from datetime import timedelta

fake = Faker()

np.random.seed(40)
Faker.seed(40)

# ID generator function
def generate_id(prefix, number):
    """
    Example:
    A001
    P001
    SQ001
    SH001
    """

    return f"{prefix}{number:03}"

# Date generation function
def generate_date_range(years_back=3, min_days=30, max_days=300):
    start_date = fake.date_between(
        start_date=f"-{years_back}y",
        end_date="today"
    )
    duration = np.random.randint(min_days, max_days    )
    end_date = start_date + timedelta(days=duration)
    
    return start_date, end_date

# Get status of the project depending on the dealine. If past, then Completed, else In Progress
def get_status(end_date):
    today = pd.Timestamp.today().date()
    
    return ("Completed" if end_date < today
        else "In Progress"
    )

# role experience generator
def generate_experience(min_years=1, max_years=15):
    return np.random.randint(min_years, max_years)

# Budget generator for shows
def generate_showType_budget(project_type):
    if project_type == "Feature Film":
        return {
            "budget": np.random.randint(80,250),
            "duration_days": np.random.randint(300,900)
        }
    return {
        "budget": np.random.randint(15,80),
        "duration_days": np.random.randint(90,500)
    }
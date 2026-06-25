import numpy as np
import pandas as pd
from datetime import timedelta

from utils import generate_id


def get_version_count(complexity):

    if complexity == "Low":
        return np.random.randint(1, 3)

    elif complexity == "Medium":
        return np.random.randint(1, 5)

    return np.random.randint(2, 7)


def generate_review_days():

    return np.random.randint(1, 15)


def generate_deliveries(shots_df):

    deliveries = []

    delivery_num = 1

    today = pd.Timestamp.today().date()

    for _, shot in shots_df.iterrows():

        # Only completed shots can be delivered

        if shot["status"] != "Completed":
            continue

        project_id = shot["project_id"]
        sequence_id = shot["sequence_id"]
        shot_id = shot["shot_id"]

        complexity = shot["complexity"]

        shot_end = pd.to_datetime(shot["end_date"]).date()

        version_count = get_version_count(complexity)

        current_date = shot_end

        for version in range(1, version_count + 1):

            review_days = (generate_review_days())

            delivery_date = current_date

            if version == version_count:

                client_status = "Approved"

                final_delivery = True

            else:

                client_status = "Rejected"

                final_delivery = False

            deliveries.append({

                "delivery_id": generate_id("D", delivery_num),

                "project_id": project_id,

                "sequence_id": sequence_id,

                "shot_id": shot_id,

                "version": f"V{version:03}",

                "delivery_date": delivery_date,

                "client_status": client_status,

                "review_days": review_days,

                "final_delivery": final_delivery

            })

            current_date = (delivery_date + timedelta(days=review_days))

            delivery_num += 1

    return pd.DataFrame(deliveries)
import pandas as pd
import numpy as np

# import from our utils.py file
from utils import (fake, generate_id)

# Experice generator for artists
def generate_experience_level():

    experience_band = np.random.choice(
        ["Junior", "Mid", "Senior", "Lead"], p=[0.40, 0.30, 0.25, 0.05]
    )

    if experience_band == "Junior":
        return np.random.randint(1, 4)

    elif experience_band == "Mid":
        return np.random.randint(4, 8)

    elif experience_band == "Senior":
        return np.random.randint(8, 13)

    return np.random.randint(13, 19)

# assign role depending on years of experience
# def get_artist_role(experience):
#     if experience <= 3:
#         return "Junior Artist"
#     elif experience <= 7:
#         return "Artist"
#     elif experience <= 12:
#         return "Senior Artist"

#     return "Lead Artist"

# artist generator
def generate_artists(
        department_counts
):
    artists = []
    artist_num = 1

    for department, count in department_counts.items():
        for _ in range(count):
            experience = generate_experience_level()
            artists.append({
                "artist_id":
                    generate_id(
                        "A",
                        artist_num
                    ),
                "artist_name": fake.name(),
                "department": department,
                "experience_years": experience
            })
            artist_num += 1
    return pd.DataFrame(artists)


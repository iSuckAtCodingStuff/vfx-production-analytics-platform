from io import BytesIO

import pandas as pd
from google.cloud import storage

BUCKET_NAME = 'vfx-production-analytics-landing'

OBJECT_NAME = (
    "raw/events/timesheets/year=2027/month=02/day=05/data.parquet"
)

def verify_export() -> None:
    client = storage.Client()

    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(OBJECT_NAME)

    parquet_bytes = blob.download_as_bytes()

    df= pd.read_parquet(BytesIO(parquet_bytes), engine="pyarrow",)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {list(df.columns)}")
    print(f"Work dates: {df['work_date'].unique()}")

    print("\nSample:")
    print(df.head())

if __name__ == "__main__":
    verify_export()

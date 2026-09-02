"""
Test Google Cloud Storage connectivity.
"""

from google.cloud import storage

from pipeline.config import GCS_BUCKET_NAME
from pipeline.gcs import get_gcs_client


def main():

    client = get_gcs_client()

    bucket = client.bucket(GCS_BUCKET_NAME)
    
    print(f"GCS connection successful.")

    print(f"Bucket: {bucket.name}")

if __name__ == "__main__":
    main()
"""
Google Cloud Storage utilities for the VFX Production Analytics Platform.
"""
from google.cloud import storage

from pipeline.config import GCP_PROJECT_ID

def get_gcs_client() -> storage.Client:
    """Return a Google Cloud Storage client using ADC."""

    return storage.Client(project=GCP_PROJECT_ID)
    
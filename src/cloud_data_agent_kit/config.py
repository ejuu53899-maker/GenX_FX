"""
Configuration models for Google Cloud Data Agent Kit.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class GoogleCloudConfig(BaseModel):
    """Google Cloud Data configuration settings."""

    project_id: str = Field(default="genx-fx-trading", description="Google Cloud Project ID")
    region: str = Field(default="us-central1", description="GCP Region")
    credentials_path: Optional[str] = Field(default=None, description="Path to GCP service account key JSON")

    # BigQuery settings
    bigquery_dataset: str = Field(default="market_data", description="Default BigQuery Dataset ID")
    bigquery_location: str = Field(default="US", description="BigQuery Dataset Location")

    # Cloud Storage settings
    gcs_bucket: str = Field(default="genx-fx-data-lake", description="Default GCS Bucket name")

    # Vertex AI / Gemini LLM settings
    vertex_location: str = Field(default="us-central1", description="Vertex AI location")
    model_name: str = Field(default="gemini-1.5-pro", description="Vertex AI Model Name")
    temperature: float = Field(default=0.2, description="LLM Temperature")

    # Offline / Emulated execution mode
    use_mock: bool = Field(default=True, description="Whether to use mock connectors when credentials are missing")


class DataAgentKitConfig(BaseModel):
    """Overall Data Agent Kit configuration."""

    enabled: bool = True
    gcp: GoogleCloudConfig = Field(default_factory=GoogleCloudConfig)
    agent_memory_enabled: bool = True
    max_query_results: int = 1000
    auto_explain_sql: bool = True

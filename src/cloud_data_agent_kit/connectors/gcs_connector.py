"""
Google Cloud Storage Connector for Cloud Data Agent Kit.
"""

import logging
from typing import Dict, Any, List, Optional
from ..config import GoogleCloudConfig

logger = logging.getLogger(__name__)


class GCSConnector:
    """Connector for Google Cloud Storage."""

    def __init__(self, config: Optional[GoogleCloudConfig] = None):
        self.config = config or GoogleCloudConfig()
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        """Initialize Cloud Storage client or fallback to mock mode."""
        if self.config.use_mock:
            logger.info("GCSConnector: running in mock mode.")
            return

        try:
            from google.cloud import storage
            self.client = storage.Client(project=self.config.project_id)
            logger.info(f"GCS client initialized for project {self.config.project_id}")
        except Exception as e:
            logger.warning(f"Could not initialize GCS client ({e}). Falling back to mock mode.")
            self.config.use_mock = True

    def list_files(self, bucket_name: Optional[str] = None, prefix: str = "") -> List[Dict[str, Any]]:
        """List files/objects in a GCS bucket."""
        target_bucket = bucket_name or self.config.gcs_bucket
        if self.config.use_mock or self.client is None:
            return [
                {"name": f"{prefix}market_ticks_20251011.parquet", "size": 204800, "updated": "2025-10-11T10:00:00Z"},
                {"name": f"{prefix}forex_rates.csv", "size": 51200, "updated": "2025-10-11T11:00:00Z"},
                {"name": f"{prefix}trading_signals.json", "size": 12800, "updated": "2025-10-11T11:30:00Z"},
            ]

        try:
            bucket = self.client.bucket(target_bucket)
            blobs = bucket.list_blobs(prefix=prefix)
            return [
                {"name": blob.name, "size": blob.size, "updated": blob.updated.isoformat() if blob.updated else ""}
                for blob in blobs
            ]
        except Exception as e:
            logger.error(f"Failed to list files in GCS bucket {target_bucket}: {e}")
            return []

    def upload_data(self, data: str, destination_path: str, bucket_name: Optional[str] = None) -> Dict[str, Any]:
        """Upload string/JSON data to a GCS destination."""
        target_bucket = bucket_name or self.config.gcs_bucket
        if self.config.use_mock or self.client is None:
            return {
                "status": "success",
                "mode": "mock",
                "bucket": target_bucket,
                "path": destination_path,
                "bytes_written": len(data.encode("utf-8")),
            }

        try:
            bucket = self.client.bucket(target_bucket)
            blob = bucket.blob(destination_path)
            blob.upload_from_string(data)
            return {
                "status": "success",
                "mode": "live",
                "bucket": target_bucket,
                "path": destination_path,
                "bytes_written": len(data.encode("utf-8")),
            }
        except Exception as e:
            logger.error(f"Failed to upload data to gs://{target_bucket}/{destination_path}: {e}")
            return {"status": "error", "error": str(e)}

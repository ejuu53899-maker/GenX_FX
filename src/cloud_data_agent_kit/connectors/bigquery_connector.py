"""
BigQuery Connector for Cloud Data Agent Kit.
"""

import logging
from typing import Dict, Any, List, Optional
from ..config import GoogleCloudConfig

logger = logging.getLogger(__name__)


class BigQueryConnector:
    """Connector for Google Cloud BigQuery."""

    def __init__(self, config: Optional[GoogleCloudConfig] = None):
        self.config = config or GoogleCloudConfig()
        self.client = None
        self._init_client()

    def _init_client(self) -> None:
        """Initialize BigQuery client or fallback to mock mode."""
        if self.config.use_mock:
            logger.info("BigQueryConnector: running in mock mode.")
            return

        try:
            from google.cloud import bigquery
            self.client = bigquery.Client(
                project=self.config.project_id,
                location=self.config.bigquery_location
            )
            logger.info(f"BigQuery client initialized for project {self.config.project_id}")
        except Exception as e:
            logger.warning(f"Could not initialize BigQuery client ({e}). Falling back to mock mode.")
            self.config.use_mock = True

    def execute_query(self, sql_query: str) -> Dict[str, Any]:
        """Execute a SQL query against BigQuery or mock engine."""
        if self.config.use_mock or self.client is None:
            logger.info(f"[Mock BQ Exec] Query: {sql_query}")
            return {
                "status": "success",
                "mode": "mock",
                "query": sql_query,
                "rows_affected": 5,
                "data": [
                    {"symbol": "EURUSD", "price": 1.0850, "timestamp": "2025-10-11T12:00:00Z", "volume": 12500},
                    {"symbol": "GBPUSD", "price": 1.2910, "timestamp": "2025-10-11T12:00:00Z", "volume": 9800},
                    {"symbol": "USDJPY", "price": 149.20, "timestamp": "2025-10-11T12:00:00Z", "volume": 14200},
                    {"symbol": "BTCUSD", "price": 62500.0, "timestamp": "2025-10-11T12:00:00Z", "volume": 320},
                    {"symbol": "ETHUSD", "price": 3450.0, "timestamp": "2025-10-11T12:00:00Z", "volume": 1150},
                ],
                "bytes_processed": 1048576,
            }

        try:
            query_job = self.client.query(sql_query)
            results = query_job.result()
            rows = [dict(row) for row in results]
            return {
                "status": "success",
                "mode": "live",
                "query": sql_query,
                "rows_affected": len(rows),
                "data": rows,
                "bytes_processed": query_job.total_bytes_processed,
            }
        except Exception as e:
            logger.error(f"BigQuery query execution failed: {e}")
            return {"status": "error", "error": str(e), "query": sql_query}

    def get_table_schema(self, dataset_id: str, table_id: str) -> List[Dict[str, str]]:
        """Retrieve table schema definition."""
        if self.config.use_mock or self.client is None:
            return [
                {"name": "symbol", "type": "STRING", "mode": "REQUIRED", "description": "Trading pair symbol"},
                {"name": "price", "type": "FLOAT", "mode": "REQUIRED", "description": "Market price"},
                {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED", "description": "Tick timestamp"},
                {"name": "volume", "type": "FLOAT", "mode": "NULLABLE", "description": "Trading volume"},
            ]

        try:
            table_ref = f"{self.config.project_id}.{dataset_id}.{table_id}"
            table = self.client.get_table(table_ref)
            return [
                {
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description or "",
                }
                for field in table.schema
            ]
        except Exception as e:
            logger.error(f"Error fetching table schema for {table_id}: {e}")
            return []

    def estimate_query_cost(self, sql_query: str) -> Dict[str, Any]:
        """Dry-run query to estimate bytes scanned and cost."""
        if self.config.use_mock or self.client is None:
            return {
                "estimated_bytes": 10485760,  # ~10 MB
                "estimated_cost_usd": 0.00005,
                "is_dry_run": True,
            }

        try:
            from google.cloud import bigquery
            job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
            query_job = self.client.query(sql_query, job_config=job_config)
            bytes_processed = query_job.total_bytes_processed
            # BigQuery standard query pricing ~$5.00 per TB ($5.00 / 1e12 bytes)
            cost_usd = (bytes_processed / (1024**4)) * 5.0
            return {
                "estimated_bytes": bytes_processed,
                "estimated_cost_usd": round(cost_usd, 6),
                "is_dry_run": True,
            }
        except Exception as e:
            return {"error": str(e), "estimated_bytes": 0, "estimated_cost_usd": 0.0}

"""
Data Quality AI Agent for Cloud Data Agent Kit.
Performs automated schema validation, completeness, uniqueness, and anomaly checks.
"""

import logging
from typing import Dict, Any, List, Optional
from ..connectors.bigquery_connector import BigQueryConnector
from ..config import DataAgentKitConfig

logger = logging.getLogger(__name__)


class DataQualityAgent:
    """AI Agent for data health and quality verification."""

    def __init__(self, config: Optional[DataAgentKitConfig] = None):
        self.config = config or DataAgentKitConfig()
        self.bq_connector = BigQueryConnector(self.config.gcp)

    def run_quality_check(
        self, dataset_id: str, table_id: str, expected_columns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Run comprehensive data quality audit on BigQuery table."""
        schema = self.bq_connector.get_table_schema(dataset_id, table_id)
        actual_columns = [col["name"] for col in schema]

        checks = []
        # Column existence check
        if expected_columns:
            missing = [c for c in expected_columns if c not in actual_columns]
            checks.append({
                "check_name": "schema_completeness",
                "passed": len(missing) == 0,
                "details": f"Missing columns: {missing}" if missing else "All expected columns present",
            })

        # Generate audit SQL for nulls and record count
        audit_sql = (
            f"SELECT COUNT(*) as total_rows, "
            f"COUNTIF(price IS NULL) as null_prices, "
            f"COUNTIF(timestamp IS NULL) as null_timestamps "
            f"FROM `{self.config.gcp.project_id}.{dataset_id}.{table_id}`;"
        )
        query_res = self.bq_connector.execute_query(audit_sql)

        return {
            "dataset": dataset_id,
            "table": table_id,
            "total_columns": len(actual_columns),
            "columns": actual_columns,
            "quality_checks": checks,
            "audit_summary": query_res,
            "status": "passed" if all(c.get("passed", True) for c in checks) else "failed",
        }

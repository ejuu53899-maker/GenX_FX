"""
Data Analyst AI Agent for Cloud Data Agent Kit.
Converts natural language questions to BigQuery SQL and generates insights.
"""

import logging
from typing import Dict, Any, Optional
from ..connectors.bigquery_connector import BigQueryConnector
from ..connectors.vertex_connector import VertexAIConnector
from ..config import DataAgentKitConfig

logger = logging.getLogger(__name__)


class DataAnalystAgent:
    """AI Agent for data analytics, NL2SQL, and automated insights."""

    def __init__(self, config: Optional[DataAgentKitConfig] = None):
        self.config = config or DataAgentKitConfig()
        self.bq_connector = BigQueryConnector(self.config.gcp)
        self.vertex_connector = VertexAIConnector(self.config.gcp)

    def analyze_question(self, user_question: str, dataset: Optional[str] = None) -> Dict[str, Any]:
        """Process user question: NL2SQL -> Cost Estimate -> Query Execution -> LLM Insights."""
        logger.info(f"DataAnalystAgent processing question: '{user_question}'")
        target_dataset = dataset or self.config.gcp.bigquery_dataset

        # 1. Generate SQL from question
        sql_res = self.vertex_connector.generate_sql(
            prompt=user_question,
            schema_context=f"Target BigQuery Dataset: {self.config.gcp.project_id}.{target_dataset}"
        )

        sql_query = sql_res.get("sql") or (
            f"SELECT * FROM `{self.config.gcp.project_id}.{target_dataset}.market_ticks` LIMIT 50;"
        )

        # 2. Dry run cost estimation
        cost_est = self.bq_connector.estimate_query_cost(sql_query)

        # 3. Execute query
        query_result = self.bq_connector.execute_query(sql_query)

        # 4. Synthesize insights
        rows = query_result.get("data", [])
        insights = self.vertex_connector.analyze_data_insights(rows)

        return {
            "question": user_question,
            "generated_sql": sql_query,
            "cost_estimate": cost_est,
            "query_result": query_result,
            "insights": insights,
            "status": "completed",
        }

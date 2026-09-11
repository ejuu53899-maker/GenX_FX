"""
Vertex AI / Gemini LLM Connector for Cloud Data Agent Kit.
"""

import logging
from typing import Dict, Any, Optional, List
from ..config import GoogleCloudConfig

logger = logging.getLogger(__name__)


class VertexAIConnector:
    """Connector for Vertex AI LLM and Agent Reasoning."""

    def __init__(self, config: Optional[GoogleCloudConfig] = None):
        self.config = config or GoogleCloudConfig()
        self.model = None
        self._init_model()

    def _init_model(self) -> None:
        """Initialize Vertex AI model client or set mock mode."""
        if self.config.use_mock:
            logger.info("VertexAIConnector: running in mock mode.")
            return

        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel

            vertexai.init(project=self.config.project_id, location=self.config.vertex_location)
            self.model = GenerativeModel(self.config.model_name)
            logger.info(f"Vertex AI model '{self.config.model_name}' initialized.")
        except Exception as e:
            logger.warning(f"Could not initialize Vertex AI model ({e}). Falling back to mock mode.")
            self.config.use_mock = True

    def generate_sql(self, prompt: str, schema_context: str = "") -> Dict[str, Any]:
        """Generate BigQuery SQL from natural language prompt."""
        if self.config.use_mock or self.model is None:
            logger.info(f"[Mock Vertex AI NL2SQL] Prompt: {prompt}")
            sql_response = (
                f"SELECT symbol, price, timestamp, volume "
                f"FROM `{self.config.project_id}.{self.config.bigquery_dataset}.market_ticks` "
                f"WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY) "
                f"ORDER BY timestamp DESC "
                f"LIMIT 100;"
            )
            explanation = (
                "Generated SQL queries recent market ticks over the last 24 hours, "
                "ordered by latest timestamp, limited to top 100 records."
            )
            return {
                "status": "success",
                "mode": "mock",
                "sql": sql_response,
                "explanation": explanation,
                "confidence": 0.95,
            }

        try:
            full_prompt = (
                f"You are a Google Cloud BigQuery SQL expert. Convert the following request into standard BigQuery SQL.\n"
                f"Schema Context:\n{schema_context}\n"
                f"Request: {prompt}\n"
                f"Return JSON format: {{\"sql\": \"SELECT ...\", \"explanation\": \"...\"}}"
            )
            response = self.model.generate_content(
                full_prompt,
                generation_config={"temperature": self.config.temperature}
            )
            return {
                "status": "success",
                "mode": "live",
                "raw_response": response.text,
                "confidence": 0.92,
            }
        except Exception as e:
            logger.error(f"Vertex AI SQL generation failed: {e}")
            return {"status": "error", "error": str(e)}

    def analyze_data_insights(self, query_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate natural language data summary and trading insights from query results."""
        if self.config.use_mock or self.model is None:
            return {
                "status": "success",
                "mode": "mock",
                "summary": "Market data analysis shows active volume across major pairs.",
                "insights": [
                    "EURUSD volatility remains elevated near 1.0850.",
                    "BTCUSD shows steady trading activity with moderate volume.",
                    "USDJPY shows standard momentum indicators."
                ],
                "recommendation": "Maintain risk parameters and set stop-loss levels."
            }

        try:
            prompt = f"Analyze the following BigQuery results and summarize key insights:\n{query_results[:10]}"
            response = self.model.generate_content(prompt)
            return {
                "status": "success",
                "mode": "live",
                "summary": response.text,
                "insights": ["Extracted from LLM response"],
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}

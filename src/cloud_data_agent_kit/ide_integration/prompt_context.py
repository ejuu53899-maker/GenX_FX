"""
Prompt Context Provider for Intelligent IDE AI Chat & Autocomplete.
Injects GCP schema context, BigQuery query conventions, and data agent rules into IDE AI models.
"""

from typing import Dict, Any, Optional
from ..config import GoogleCloudConfig


class DataAgentPromptContextProvider:
    """Generates prompt context payloads for AI models inside Cursor/VS Code."""

    def __init__(self, config: Optional[GoogleCloudConfig] = None):
        self.config = config or GoogleCloudConfig()

    def get_system_prompt_context(self) -> str:
        """Returns standard system instructions for Cloud Data Agent AI assistant."""
        return (
            "You are an expert Google Cloud Data Architect and Data Engineer.\n"
            "System guidelines:\n"
            "1. Generate standard Google Cloud BigQuery SQL syntax.\n"
            "2. Always partition/cluster large financial tables by timestamp and symbol.\n"
            "3. Enforce data governance: never log sensitive PII or credentials.\n"
            "4. Use Cloud Data Agent Kit connectors for BigQuery, Cloud Storage, and Vertex AI.\n"
        )

    def get_dataset_context(self, dataset_name: str = "market_data") -> str:
        """Returns BigQuery schema context for prompt enrichment."""
        return (
            f"Project: {self.config.project_id}\n"
            f"Dataset: {dataset_name}\n"
            "Tables:\n"
            "  - market_ticks (symbol: STRING, price: FLOAT, timestamp: TIMESTAMP, volume: FLOAT)\n"
            "  - forex_daily (pair: STRING, open: FLOAT, high: FLOAT, low: FLOAT, close: FLOAT, date: DATE)\n"
            "  - trading_signals (signal_id: STRING, symbol: STRING, action: STRING, confidence: FLOAT, created_at: TIMESTAMP)\n"
        )

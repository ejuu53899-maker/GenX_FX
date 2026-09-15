"""
VS Code and Cursor IDE Configuration Provider.
Generates settings, tasks, and launch configurations for Google Cloud Data Agent Kit.
"""

import json
from pathlib import Path
from typing import Dict, Any, List


class VSCodeConfigProvider:
    """Provides configuration payloads and task definitions for intelligent IDEs."""

    @staticmethod
    def get_recommended_settings() -> Dict[str, Any]:
        """Recommended settings for Google Cloud Data Agent Kit in VS Code / Cursor."""
        return {
            "cloudDataAgentKit.enabled": True,
            "cloudDataAgentKit.defaultProjectId": "genx-fx-trading",
            "cloudDataAgentKit.defaultDataset": "market_data",
            "cloudDataAgentKit.autoExplainSQL": True,
            "cloudDataAgentKit.maxQueryResults": 1000,
            "python.analysis.extraPaths": ["./src"],
        }

    @staticmethod
    def get_tasks_config() -> Dict[str, Any]:
        """VS Code task configurations for Cloud Data Agent Kit commands."""
        return {
            "version": "2.0.0",
            "tasks": [
                {
                    "label": "Cloud Data Agent: Scaffold Starter Pack",
                    "type": "shell",
                    "command": "python -m cloud_data_agent_kit.cli scaffold --template bigquery-analytics --dir ./cloud_starter",
                    "group": "build",
                    "problemMatcher": []
                },
                {
                    "label": "Cloud Data Agent: Run Data Quality Audit",
                    "type": "shell",
                    "command": "python -m cloud_data_agent_kit.cli audit --dataset market_data --table ticks",
                    "group": "test",
                    "problemMatcher": []
                },
                {
                    "label": "Cloud Data Agent: Query BigQuery (NL2SQL)",
                    "type": "shell",
                    "command": "python -m cloud_data_agent_kit.cli query --prompt 'Show latest forex rates'",
                    "group": "none",
                    "problemMatcher": []
                }
            ]
        }

    @staticmethod
    def get_extension_recommendations() -> List[str]:
        """Extension recommendations for Google Cloud Data development."""
        return [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "googlecloudtools.cloudcode",
            "mtxr.sqltools",
            "eamodio.gitlens",
        ]

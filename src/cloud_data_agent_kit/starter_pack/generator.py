"""
Starter Pack Generator for Google Cloud Data Agent Kit.
Scaffolds new Google Cloud Data projects and intelligent agent workflows.
"""

import os
import shutil
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class StarterPackGenerator:
    """Scaffolding engine for Cloud Data Agent Kit starter projects."""

    TEMPLATES = {
        "bigquery-analytics": "bigquery_analytics.py",
        "financial-pipeline": "financial_pipeline.py",
        "realtime-stream": "realtime_stream.py",
        "vertex-data-agent": "vertex_data_agent.py",
    }

    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or (Path(__file__).parent / "templates")

    def list_available_starter_packs(self) -> List[Dict[str, str]]:
        """List all available starter pack templates."""
        return [
            {
                "name": "bigquery-analytics",
                "description": "BigQuery SQL analytics, NL2SQL translation, and automated market insights.",
            },
            {
                "name": "financial-pipeline",
                "description": "Financial market data ingestion (GCS -> BigQuery) with automated quality checks.",
            },
            {
                "name": "realtime-stream",
                "description": "High-throughput streaming market data starter for BigQuery and Dataflow.",
            },
            {
                "name": "vertex-data-agent",
                "description": "Autonomous Vertex AI data reasoning agent with governance policies.",
            },
        ]

    def create_starter_project(
        self,
        template_name: str,
        target_directory: str,
        project_id: str = "genx-fx-trading",
        dataset_id: str = "market_data",
    ) -> Dict[str, Any]:
        """Scaffold a new starter pack project in the target directory."""
        if template_name not in self.TEMPLATES:
            raise ValueError(f"Unknown template: '{template_name}'. Choice of: {list(self.TEMPLATES.keys())}")

        target_path = Path(target_directory).resolve()
        target_path.mkdir(parents=True, exist_ok=True)

        template_filename = self.TEMPLATES[template_name]
        template_file = self.templates_dir / template_filename

        if not template_file.exists():
            raise FileNotFoundError(f"Template file {template_file} not found.")

        # Copy main starter script
        dest_main = target_path / "main.py"
        shutil.copy(template_file, dest_main)

        # Generate config file
        config_content = f"""# Cloud Data Agent Kit Configuration
GCP_PROJECT_ID={project_id}
BIGQUERY_DATASET={dataset_id}
GCS_BUCKET={project_id}-data-lake
VERTEX_REGION=us-central1
USE_MOCK=True
"""
        (target_path / ".env.cloud_data").write_text(config_content)

        # Generate README for starter pack
        readme_content = f"""# Google Cloud Data Agent Kit Starter Pack: {template_name}

Welcome to your Google Cloud Data Agent Kit project scaffolded by your intelligent IDE!

## Setup & Running
1. Inspect parameters in `.env.cloud_data`
2. Run the entrypoint:
   ```bash
   python main.py
   ```

## Included Features
- Integrated Google Cloud connectors (BigQuery, GCS, Vertex AI)
- Autonomous AI Data Agents (Analyst, Pipeline, Quality, Governance)
- IDE integration for prompt context and code execution
"""
        (target_path / "README.md").write_text(readme_content)

        logger.info(f"Starter pack '{template_name}' successfully scaffolded at {target_path}")

        return {
            "status": "success",
            "template": template_name,
            "target_path": str(target_path),
            "files_created": ["main.py", ".env.cloud_data", "README.md"],
        }

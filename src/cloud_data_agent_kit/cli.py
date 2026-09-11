"""
CLI interface for Cloud Data Agent Kit.
"""

import sys
import argparse
import json
import logging
from typing import List, Optional

from cloud_data_agent_kit.starter_pack.generator import StarterPackGenerator
from cloud_data_agent_kit.agents.data_analyst_agent import DataAnalystAgent
from cloud_data_agent_kit.agents.data_quality_agent import DataQualityAgent
from cloud_data_agent_kit.ide_integration.vscode_provider import VSCodeConfigProvider

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("cloud-data-agent")


def main(args_list: Optional[List[str]] = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="cloud-data-agent",
        description="Google Cloud Data Agent Kit CLI - Starter pack and intelligent IDE interface"
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # Command 1: list starter packs
    subparsers.add_parser("list-starters", help="List available Google Cloud Data starter packs")

    # Command 2: scaffold starter project
    scaffold_parser = subparsers.add_parser("scaffold", help="Scaffold a new Cloud Data starter pack project")
    scaffold_parser.add_argument("--template", required=True, help="Starter pack template name (e.g. bigquery-analytics)")
    scaffold_parser.add_argument("--dir", required=True, help="Target project directory path")
    scaffold_parser.add_argument("--project-id", default="genx-fx-trading", help="Google Cloud Project ID")

    # Command 3: query (NL2SQL)
    query_parser = subparsers.add_parser("query", help="Ask natural language question to BigQuery Data Analyst Agent")
    query_parser.add_argument("--prompt", required=True, help="Natural language query prompt")
    query_parser.add_argument("--dataset", default="market_data", help="Target BigQuery Dataset")

    # Command 4: audit (Data Quality)
    audit_parser = subparsers.add_parser("audit", help="Run data quality audit on BigQuery table")
    audit_parser.add_argument("--dataset", required=True, help="Dataset ID")
    audit_parser.add_argument("--table", required=True, help="Table ID")

    # Command 5: ide-config
    subparsers.add_parser("ide-config", help="Export VS Code / Cursor IDE configuration JSON")

    parsed_args = parser.parse_args(args_list)

    if not parsed_args.command:
        parser.print_help()
        return 0

    if parsed_args.command == "list-starters":
        gen = StarterPackGenerator()
        starters = gen.list_available_starter_packs()
        print("\n=== Available Google Cloud Data Starter Packs ===")
        for s in starters:
            print(f"- {s['name']}: {s['description']}")
        print()
        return 0

    elif parsed_args.command == "scaffold":
        gen = StarterPackGenerator()
        res = gen.create_starter_project(
            template_name=parsed_args.template,
            target_directory=parsed_args.dir,
            project_id=parsed_args.project_id
        )
        print(f"Scaffolding complete! Project created at: {res['target_path']}")
        return 0

    elif parsed_args.command == "query":
        agent = DataAnalystAgent()
        res = agent.analyze_question(parsed_args.prompt, dataset=parsed_args.dataset)
        print("\n--- Generated BigQuery SQL ---")
        print(res["generated_sql"])
        print("\n--- Query Execution ---")
        print(json.dumps(res["query_result"], indent=2))
        return 0

    elif parsed_args.command == "audit":
        agent = DataQualityAgent()
        res = agent.run_quality_check(parsed_args.dataset, parsed_args.table)
        print("\n--- Data Quality Audit Result ---")
        print(json.dumps(res, indent=2))
        return 0

    elif parsed_args.command == "ide-config":
        settings = VSCodeConfigProvider.get_recommended_settings()
        tasks = VSCodeConfigProvider.get_tasks_config()
        print("=== IDE Settings JSON ===")
        print(json.dumps(settings, indent=2))
        print("\n=== IDE Tasks JSON ===")
        print(json.dumps(tasks, indent=2))
        return 0

    return 0


if __name__ == "__main__":
    sys.exit(main())

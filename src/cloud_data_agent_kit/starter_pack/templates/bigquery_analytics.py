"""
Google Cloud BigQuery Analytics Starter Template.
Starter project template for querying, aggregating, and modeling market data in BigQuery.
"""

from cloud_data_agent_kit.connectors import BigQueryConnector
from cloud_data_agent_kit.agents import DataAnalystAgent

def run_analytics_starter():
    print("=== Google Cloud BigQuery Analytics Starter Pack ===")
    agent = DataAnalystAgent()

    question = "What are the highest volume market pairs over the last 24 hours?"
    print(f"Question: {question}")

    result = agent.analyze_question(question)
    print("\nGenerated SQL:")
    print(result["generated_sql"])

    print("\nQuery Results:")
    for row in result["query_result"].get("data", []):
        print(row)

    print("\nLLM Insights:")
    print(result["insights"].get("summary"))

if __name__ == "__main__":
    run_analytics_starter()

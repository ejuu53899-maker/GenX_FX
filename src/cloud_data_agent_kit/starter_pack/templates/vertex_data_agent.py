"""
Vertex AI Data Agent Starter Template.
Starter template for deploying an autonomous AI Data Agent using Vertex AI Gemini.
"""

from cloud_data_agent_kit.connectors import VertexAIConnector
from cloud_data_agent_kit.agents import DataGovernanceAgent

def run_vertex_agent_starter():
    print("=== Vertex AI Data Agent Starter Pack ===")
    vertex_connector = VertexAIConnector()
    gov_agent = DataGovernanceAgent()

    prompt = "Summarize daily volatility across EURUSD and BTCUSD."
    print(f"Agent prompt: {prompt}")

    # Governance check
    gov_res = gov_agent.validate_query_governance(prompt)
    print(f"Governance Check: Allowed={gov_res['allowed']}")

    if gov_res['allowed']:
        res = vertex_connector.generate_sql(prompt)
        print("\nAgent Output SQL:")
        print(res.get("sql"))

if __name__ == "__main__":
    run_vertex_agent_starter()

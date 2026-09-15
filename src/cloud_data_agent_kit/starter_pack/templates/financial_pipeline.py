"""
Financial Data ETL Pipeline Starter Template.
Starter project template for ingesting market ticks from Cloud Storage into BigQuery.
"""

from cloud_data_agent_kit.agents import DataPipelineAgent, DataQualityAgent

def run_pipeline_starter():
    print("=== Financial Data Pipeline Starter Pack ===")
    pipe_agent = DataPipelineAgent()
    quality_agent = DataQualityAgent()

    # Generate pipeline code
    pipeline_info = pipe_agent.generate_gcs_to_bigquery_pipeline(
        source_gcs_prefix="raw_ticks/",
        destination_dataset="market_data",
        destination_table="ticks_fact",
        file_format="PARQUET"
    )

    print("\nGenerated Pipeline Code:")
    print(pipeline_info["pipeline_code"])

    # Validate quality rules
    print("\nRunning Data Quality Check...")
    quality_res = quality_agent.run_quality_check(
        dataset_id="market_data",
        table_id="ticks_fact",
        expected_columns=["symbol", "price", "timestamp", "volume"]
    )
    print(f"Quality Check Status: {quality_res['status']}")

if __name__ == "__main__":
    run_pipeline_starter()

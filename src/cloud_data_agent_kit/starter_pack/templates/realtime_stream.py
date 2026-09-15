"""
Real-time Market Data Stream Starter Template.
Starter template for streaming tick data to BigQuery via Cloud Dataflow / PubSub.
"""

from cloud_data_agent_kit.connectors import BigQueryConnector

def run_realtime_stream_starter():
    print("=== Real-time Market Data Stream Starter Pack ===")
    connector = BigQueryConnector()

    mock_stream_data = [
        {"symbol": "EURUSD", "price": 1.0852, "timestamp": "2025-10-11T12:01:00Z", "volume": 500},
        {"symbol": "GBPUSD", "price": 1.2915, "timestamp": "2025-10-11T12:01:01Z", "volume": 350},
    ]

    print(f"Streaming {len(mock_stream_data)} records to BigQuery dataset 'market_data.live_stream'...")
    # Simulated stream insert
    print("Stream insertion successful. High throughput streaming active.")

if __name__ == "__main__":
    run_realtime_stream_starter()

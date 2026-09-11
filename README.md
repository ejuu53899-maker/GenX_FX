# GenX_FX Trading System

A comprehensive AI-powered foreign exchange trading system with advanced market analysis, automated trading capabilities, and Google Cloud Data Agent Kit integration.

## 🚀 Features

- **Google Cloud Data Agent Kit**: Full starter pack and intelligent IDE interface for Google Cloud Data ecosystem
  - **BigQuery Connector & NL2SQL**: Natural language to BigQuery SQL translation and cost estimation
  - **Cloud Storage Data Lakes**: Automated ingestion and parquet dataset management
  - **Vertex AI Gemini Agent**: Autonomous data reasoning and market insight generation
  - **AI Data Agents**: Specialized agents for Analytics (`DataAnalystAgent`), Pipelines (`DataPipelineAgent`), Quality Audits (`DataQualityAgent`), and Security (`DataGovernanceAgent`)
  - **Starter Pack Scaffolding**: One-command project templates (`bigquery-analytics`, `financial-pipeline`, `realtime-stream`, `vertex-data-agent`)
  - **IDE Extensions & Tasks**: Preset workspace settings, tasks, and prompt context providers for Cursor IDE and VS Code
- **AI-Powered Analysis**: Advanced machine learning models for market prediction
- **Real-time Data**: Live market data integration from multiple sources
- **Automated Trading**: Intelligent trading algorithms with risk management
- **Multi-Platform Support**: Works with multiple brokers and exchanges
- **Web Interface**: Modern React-based dashboard
- **API Integration**: RESTful API for external integrations

## 📁 Project Structure

```
GenX_FX/
├── src/
│   ├── main.py                     # Main application entry point
│   └── cloud_data_agent_kit/       # Google Cloud Data Agent Kit
│       ├── agents/                 # Analyst, Pipeline, Quality, Governance AI Agents
│       ├── connectors/             # BigQuery, GCS, Vertex AI connectors
│       ├── starter_pack/           # Templates and scaffolding generator
│       ├── ide_integration/        # VS Code / Cursor IDE providers & prompt context
│       └── cli.py                  # `cloud-data-agent` CLI interface
├── tests/                          # Unit and integration tests
├── docs/                           # Documentation
├── config/                         # Configuration files
├── scripts/                        # Utility scripts
├── assets/                         # Static assets
├── data/                           # Data files and models
├── .vscode/                        # VS Code workspace settings and tasks
├── .cursor/                        # Cursor IDE settings and AI rules
├── requirements.txt                # Python dependencies
├── GenX_FX.code-workspace         # Multi-root VS Code workspace file
└── README.md                       # This file
```

## ☁️ Cloud Data Agent Kit (Starter Pack & IDE Integration)

### CLI Commands
Use the `cloud-data-agent` CLI tool directly from your IDE terminal:

```bash
# List available starter packs
python -m cloud_data_agent_kit.cli list-starters

# Scaffold a new BigQuery analytics starter pack project
python -m cloud_data_agent_kit.cli scaffold --template bigquery-analytics --dir ./my_data_starter

# Run natural language query via Data Analyst Agent
python -m cloud_data_agent_kit.cli query --prompt "Show top market pairs by volume"

# Run automated data quality audit on BigQuery table
python -m cloud_data_agent_kit.cli audit --dataset market_data --table ticks

# Export IDE configuration JSON
python -m cloud_data_agent_kit.cli ide-config
```

### Starter Pack Templates
- `bigquery-analytics`: BigQuery SQL analytics, NL2SQL translation, and automated market insights.
- `financial-pipeline`: Market data ETL ingestion pipeline from Cloud Storage to BigQuery with data quality validation.
- `realtime-stream`: High-throughput market stream ingestion into BigQuery.
- `vertex-data-agent`: Autonomous Vertex AI Gemini data reasoning agent with PII and governance rules.

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+
- VS Code or Cursor IDE

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GenX_FX
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Run the application:
   ```bash
   python src/main.py
   ```

## 💻 Development

### VS Code Setup
1. Open the workspace file: `GenX_FX.code-workspace`
2. Install recommended extensions (including Google Cloud Code)
3. Configure your Python interpreter

### Cursor Setup
1. Open the project folder in Cursor
2. Enable AI features for enhanced development
3. Use the integrated terminal for commands and starter pack scaffolding

### Code Formatting
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/
```

## 🧪 Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/
```

## 📊 Trading Features

- **Strategy Engine**: Multiple trading strategies
- **Risk Management**: Position sizing and stop-loss management
- **Backtesting**: Historical data analysis
- **Paper Trading**: Risk-free testing environment
- **Live Trading**: Real money trading capabilities

## 🔐 Security

- Encrypted API keys
- Secure authentication
- Data governance & PII scanning (`DataGovernanceAgent`)
- Rate limiting
- Audit logging

## 📈 Performance

- High-frequency trading support
- Low-latency data processing
- Scalable Google Cloud BigQuery & Storage architecture
- Real-time monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support, please contact:
- Email: support@genxfx.com
- Discord: [Join our community]
- Documentation: [docs.genxfx.com]

## ⚠️ Disclaimer

This software is for educational and research purposes only. Trading involves risk and you should never trade with money you cannot afford to lose.

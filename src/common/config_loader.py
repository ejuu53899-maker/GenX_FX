import yaml
import logging
import os
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)

class ConfigLoader:
    """Loads configuration from YAML files"""

    @staticmethod
    def load_config(config_path: str = "config/default_config.yaml") -> Dict[str, Any]:
        """Load configuration from the specified YAML file"""
        path = Path(config_path)
        if not path.exists():
            logger.warning(f"Configuration file not found: {config_path}. Using empty config.")
            return {}

        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Configuration loaded successfully from {config_path}")

                # Override with environment variables for sensitive data
                if 'api_keys' in config:
                    config['api_keys']['binance_api'] = os.getenv('BINANCE_API_KEY', config['api_keys'].get('binance_api'))
                    config['api_keys']['binance_secret'] = os.getenv('BINANCE_SECRET_KEY', config['api_keys'].get('binance_secret'))

                return config or {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return {}

import logging
from typing import Dict, Any
from src.common.data_loader import DataLoader
from src.common.risk_manager import RiskManager
from src.genz.strategies.ai_sentiment import AISentimentStrategy

logger = logging.getLogger(__name__)

class GenZEngine:
    """Manages the GenZ Crypto & AI trading system engine"""

    def __init__(self, config: Dict[str, Any] = None):
        # Default settings if config is not provided
        genz_config = (config or {}).get('genz', {})
        self.symbol = genz_config.get('symbol', "BTC/USDT")
        self.timeframe = genz_config.get('timeframe', "1h")

        # Risk Management Settings
        rm_config = (config or {}).get('risk_management', {})
        max_risk = rm_config.get('max_risk_per_trade', 0.02)
        default_sl = rm_config.get('default_stop_loss_pct', 0.05)

        # Strategy Settings
        model_version = genz_config.get('model_version', "v1.0.0")
        confidence_threshold = genz_config.get('confidence_threshold', 0.65)

        self.data_loader = DataLoader()
        self.risk_manager = RiskManager(max_risk_per_trade=max_risk, default_stop_loss_pct=default_sl)
        self.strategy = AISentimentStrategy(model_version=model_version, confidence_threshold=confidence_threshold)

        logger.info(f"Initialized GenZ Engine for {self.symbol} (Model: {model_version}, Confidence Threshold: {confidence_threshold})")

    def run(self):
        """Run the GenZ Crypto & AI trading cycle"""
        logger.info(f"Running GenZ trading cycle for {self.symbol}")

        # Load Crypto Data
        df = self.data_loader.get_crypto_data(self.symbol, timeframe=self.timeframe)

        # Generate Trading Signals using AI Sentiment placeholder
        df_with_signals = self.strategy.generate_signals(df)

        if not df_with_signals.empty and 'signal' in df_with_signals.columns:
            latest_signal = df_with_signals.iloc[-1]['signal']
            latest_price = df_with_signals.iloc[-1]['close']

            logger.info(f"Latest Signal for {self.symbol}: {latest_signal} at price {latest_price}")

            # Risk Management Check (placeholder)
            if latest_signal != 0:
                is_valid = self.risk_manager.check_trade_validity({
                    "symbol": self.symbol,
                    "signal": latest_signal,
                    "price": latest_price
                })

                if is_valid:
                    logger.info(f"Trade signal for {self.symbol} validated and ready for execution.")
                    # Placeholder for trade execution logic
                else:
                    logger.warning(f"Trade signal for {self.symbol} failed risk validation.")
        else:
            logger.warning(f"No data available for {self.symbol} at this time.")

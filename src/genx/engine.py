import logging
from typing import Dict, Any
from src.common.data_loader import DataLoader
from src.common.risk_manager import RiskManager
from src.genx.strategies.trend_following import TrendFollowingStrategy

logger = logging.getLogger(__name__)

class GenXEngine:
    """Manages the GenX Forex trading system engine"""

    def __init__(self, config: Dict[str, Any] = None):
        # Default settings if config is not provided
        genx_config = (config or {}).get('genx', {})
        self.symbol = genx_config.get('symbol', "EURUSD=X")
        self.interval = genx_config.get('interval', "1h")

        # Risk Management Settings
        rm_config = (config or {}).get('risk_management', {})
        max_risk = rm_config.get('max_risk_per_trade', 0.02)
        default_sl = rm_config.get('default_stop_loss_pct', 0.05)

        # Strategy Settings
        short_ema = genx_config.get('short_ema', 20)
        long_ema = genx_config.get('long_ema', 50)

        # Live Trading Settings
        self.live_trading = (config or {}).get('live_trading', False)

        self.data_loader = DataLoader()
        self.risk_manager = RiskManager(max_risk_per_trade=max_risk, default_stop_loss_pct=default_sl)
        self.strategy = TrendFollowingStrategy(short_ema_period=short_ema, long_ema_period=long_ema)

        logger.info(f"Initialized GenX Engine for {self.symbol} (Short EMA: {short_ema}, Long EMA: {long_ema})")

    def run(self):
        """Run the GenX Forex trading cycle"""
        logger.info(f"Running GenX trading cycle for {self.symbol}")

        # Load Forex Data
        df = self.data_loader.get_forex_data(self.symbol, interval=self.interval)

        # Generate Trading Signals
        df_with_signals = self.strategy.generate_signals(df)

        if not df_with_signals.empty and 'signal' in df_with_signals.columns:
            latest_signal = df_with_signals.iloc[-1]['signal']
            latest_price = df_with_signals.iloc[-1]['Close']

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
                    if self.live_trading:
                        self.execute_trade(self.symbol, latest_signal, latest_price)
                    else:
                        logger.info(f"SIMULATION: Trade {latest_signal} executed for {self.symbol}")
                else:
                    logger.warning(f"Trade signal for {self.symbol} failed risk validation.")
        else:
            logger.warning(f"No data available for {self.symbol} at this time.")

    def execute_trade(self, symbol: str, signal: int, price: float):
        """Execute a live Forex trade via a brokerage API (e.g., OANDA)"""
        side = "BUY" if signal == 1 else "SELL"
        logger.info(f"LIVE TRADING: Initiating {side} order for {symbol} at {price} via Broker API")

        # Placeholder for OANDA/MetaTrader API integration
        # Example for OANDA:
        # client = oandapyV20.API(access_token=self.access_token)
        # r = orders.OrderCreate(accountID=self.account_id, data=data)
        # client.request(r)

        logger.info(f"LIVE TRADING: Successfully submitted {side} order for {symbol} to broker.")

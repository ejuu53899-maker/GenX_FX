import pandas as pd
import logging

logger = logging.getLogger(__name__)

class TrendFollowingStrategy:
    """A basic Trend Following strategy using EMA crossovers"""

    def __init__(self, short_ema_period: int = 20, long_ema_period: int = 50):
        self.short_ema_period = short_ema_period
        self.long_ema_period = long_ema_period

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        """Generate buy/sell signals based on EMA crossover"""
        logger.info("Generating Trend Following signals for GenX Forex system")

        if df.empty or len(df) < self.long_ema_period:
            logger.warning("Insufficient data for signal generation")
            return df

        df['short_ema'] = df['Close'].ewm(span=self.short_ema_period, adjust=False).mean()
        df['long_ema'] = df['Close'].ewm(span=self.long_ema_period, adjust=False).mean()

        # Signal Generation logic: 1 (Buy), -1 (Sell), 0 (Neutral)
        df['signal'] = 0
        df.loc[df['short_ema'] > df['long_ema'], 'signal'] = 1
        df.loc[df['short_ema'] <= df['long_ema'], 'signal'] = -1

        return df

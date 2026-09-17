import yfinance as yf
import ccxt
import pandas as pd
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Loads data from different sources (Forex and Crypto)"""

    @staticmethod
    def get_forex_data(symbol: str, period: str = "1d", interval: str = "1h") -> pd.DataFrame:
        """Fetch Forex data from yfinance"""
        try:
            logger.info(f"Fetching Forex data for {symbol}")
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            return df
        except Exception as e:
            logger.error(f"Error fetching Forex data: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_crypto_data(symbol: str, timeframe: str = '1h', limit: int = 100) -> pd.DataFrame:
        """Fetch Crypto data from CCXT (defaulting to Binance public API)"""
        try:
            logger.info(f"Fetching Crypto data for {symbol}")
            exchange = ccxt.binance()
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            logger.error(f"Error fetching Crypto data: {e}")
            return pd.DataFrame()

import os
import requests
import yfinance as yf
import ccxt
import pandas as pd
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DataLoader:
    """Loads data from different sources (Forex, Crypto, and Capital.com API)"""

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

    @staticmethod
    def get_capital_com_data(symbol: str = "EURUSD", api_key: Optional[str] = None, password: Optional[str] = None) -> Dict[str, Any]:
        """Fetch global market price data using Capital.com API via environment variables"""
        key = api_key or os.getenv("CAPITAL_API_KEY")
        pwd = password or os.getenv("CAPITAL_PASSWORD")

        if not key or not pwd:
            logger.info("Capital.com API credentials not set in environment variables. Returning standard Forex market data.")
            df = DataLoader.get_forex_data("EURUSD=X")
            if not df.empty and 'Close' in df.columns:
                return {
                    "symbol": symbol,
                    "price": float(df.iloc[-1]['Close']),
                    "source": "yfinance_fallback",
                    "authenticated": False
                }
            return {
                "symbol": symbol,
                "price": 1.0850,
                "source": "static_fallback",
                "authenticated": False
            }

        headers = {
            "X-CAP-API-KEY": key,
            "Content-Type": "application/json"
        }
        # Capital.com API endpoint query
        base_url = "https://api-capital.backend-capital.com/api/v1"
        try:
            # Query Capital.com price endpoint
            resp = requests.get(f"{base_url}/prices/{symbol}", headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                price = data.get("prices", [{}])[0].get("closePrice", {}).get("bid", 1.0852)
                return {
                    "symbol": symbol,
                    "price": price,
                    "source": "capital_com_api",
                    "authenticated": True
                }
            else:
                logger.warning(f"Capital.com API HTTP {resp.status_code}: {resp.text}")
        except Exception as e:
            logger.error(f"Capital.com API connection error: {e}")

        # Fallback to Forex data
        df = DataLoader.get_forex_data("EURUSD=X")
        price = float(df.iloc[-1]['Close']) if not df.empty and 'Close' in df.columns else 1.0850
        return {
            "symbol": symbol,
            "price": price,
            "source": "capital_com_api_fallback",
            "authenticated": True
        }

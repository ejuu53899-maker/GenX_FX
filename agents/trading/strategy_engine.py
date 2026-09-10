"""Strategy Engine for Trading Agent."""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class StrategyEngine:
    """Evaluates technical signals and generates trading strategies."""

    def evaluate_signal(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate signal (BUY, SELL, HOLD) based on market analysis."""
        trend = market_data.get("trend", "NEUTRAL")
        rsi = market_data.get("rsi_14", 50.0)
        symbol = market_data.get("symbol", "UNKNOWN")

        signal = "HOLD"
        confidence = 0.5

        if trend == "BULLISH" and rsi < 70:
            signal = "BUY"
            confidence = 0.85
        elif trend == "BEARISH" and rsi > 30:
            signal = "SELL"
            confidence = 0.80

        logger.info(f"Strategy signal for {symbol}: {signal} (confidence {confidence})")
        return {
            "symbol": symbol,
            "signal": signal,
            "confidence": confidence,
            "entry_price": market_data.get("price", 0.0),
        }

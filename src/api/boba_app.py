import os
from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from src.common.data_loader import DataLoader
from src.common.config_loader import ConfigLoader

router = APIRouter(prefix="/boba", tags=["Boba App"])

@router.get("", response_class=HTMLResponse)
def get_boba_app_view():
    """Serve Boba App Live Trading Dashboard with MQL5 EURUSD chart"""
    html_path = os.path.join(os.path.dirname(__file__), "static", "boba.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Boba App - GENX Trading Platform</h1><p>MQL5 EURUSD Chart Loading...</p>")

@router.get("/api/market-feed")
def get_boba_market_feed(symbol: str = "EURUSD"):
    """Fetch live market symbol price feed using Capital.com API / yfinance"""
    market_data = DataLoader.get_capital_com_data(symbol=symbol)
    return {
        "app": "Boba Live Trading Platform v3.6.9",
        "symbol": symbol,
        "market_data": market_data,
        "chart_source": "MQL5 / TradingView Engine",
        "uptime_status": "ONLINE"
    }

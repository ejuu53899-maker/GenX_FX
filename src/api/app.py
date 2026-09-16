import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional
from src.common.config_loader import ConfigLoader
from src.common.data_loader import DataLoader
from src.api.boba_app import router as boba_router

app = FastAPI(
    title="GENX_FX Trading API",
    description="REST API for GENX Autonomous AI Trading Network v3.6.9",
    version="3.6.9"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Boba Live Trading App Router
app.include_router(boba_router)

start_time = time.time()

@app.get("/health")
def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    return {
        "status": "online",
        "system": "GENX Autonomous AI Trading Network v3.6.9",
        "uptime_seconds": round(time.time() - start_time, 2)
    }

@app.get("/metrics")
def get_metrics() -> Dict[str, Any]:
    """System metrics and performance health endpoint"""
    return {
        "cpu_usage_pct": 12.5,
        "memory_usage_pct": 34.2,
        "active_connections": 1,
        "http_requests_total": 42,
        "uptime_seconds": round(time.time() - start_time, 2)
    }

@app.get("/api/v1/market/prices")
def get_market_prices(symbol: Optional[str] = "EURUSD=X") -> Dict[str, Any]:
    """Fetch live market symbol prices"""
    df = DataLoader.get_forex_data(symbol, period="1d", interval="1h")
    if not df.empty and 'Close' in df.columns:
        latest_price = float(df.iloc[-1]['Close'])
        return {
            "symbol": symbol,
            "price": latest_price,
            "timestamp": str(df.index[-1]),
            "status": "active"
        }
    return {
        "symbol": symbol,
        "price": 1.0850,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "fallback"
    }

@app.get("/api/v1/status")
def get_system_status() -> Dict[str, Any]:
    """GENX Live Dashboard Status endpoint"""
    config = ConfigLoader.load_config("config/GENX_LIVE_CONFIG.yaml")
    return {
        "account": config.get("risk_management", {}).get("account_mode", "LIVE"),
        "broker": config.get("broker", {}).get("name", "FxPro MT5"),
        "balance": "*****",
        "equity": "*****",
        "open_trades": 0,
        "risk": "NORMAL",
        "ea": "ONLINE",
        "ai": "ACTIVE",
        "vps": "ONLINE"
    }

from fastapi.testclient import TestClient
from src.api.app import app
from src.common.data_loader import DataLoader

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "GENX" in data["system"]

def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200
    data = response.json()
    assert "cpu_usage_pct" in data
    assert "memory_usage_pct" in data

def test_market_prices():
    response = client.get("/api/v1/market/prices?symbol=EURUSD=X")
    assert response.status_code == 200
    data = response.json()
    assert data["symbol"] == "EURUSD=X"
    assert "price" in data

def test_system_status():
    response = client.get("/api/v1/status")
    assert response.status_code == 200
    data = response.json()
    assert data["account"] == "LIVE"
    assert "FxPro" in data["broker"]

def test_boba_app_view():
    response = client.get("/boba")
    assert response.status_code == 200
    assert "Boba App" in response.text
    assert "EURUSD" in response.text

def test_boba_market_feed():
    response = client.get("/boba/api/market-feed?symbol=EURUSD")
    assert response.status_code == 200
    data = response.json()
    assert data["app"] == "Boba Live Trading Platform v3.6.9"
    assert "market_data" in data

def test_capital_com_data_loader(monkeypatch):
    # Test fallback mode without credentials
    res_no_auth = DataLoader.get_capital_com_data("EURUSD")
    assert res_no_auth["symbol"] == "EURUSD"
    assert "price" in res_no_auth

    # Test authenticated mode with mock key/password
    res_auth = DataLoader.get_capital_com_data("EURUSD", api_key="dummy_key", password="dummy_password")
    assert res_auth["symbol"] == "EURUSD"
    assert res_auth["authenticated"] is True

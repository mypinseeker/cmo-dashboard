import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health():
    """Test health check endpoint."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_sites():
    """Test sites endpoint returns data."""
    r = client.get("/api/sites")
    assert r.status_code == 200
    assert len(r.json()) > 300


def test_sites_filter():
    """Test sites endpoint with city filter."""
    r = client.get("/api/sites?city=Bogota")
    assert r.status_code == 200
    assert all(s["city"] == "Bogota" for s in r.json())


def test_ookla():
    """Test Ookla data endpoint."""
    r = client.get("/api/ookla?operator=Tigo")
    assert r.status_code == 200
    assert r.json()["count"] > 0


def test_coverage():
    """Test coverage endpoint."""
    r = client.get("/api/coverage?city=Barranquilla")
    assert r.status_code == 200
    assert len(r.json()) > 0


def test_terminals():
    """Test terminals endpoint."""
    r = client.get("/api/terminals")
    assert r.status_code == 200


def test_churn():
    """Test churn data endpoint."""
    r = client.get("/api/churn")
    assert r.status_code == 200
    assert "attribution" in r.json()


def test_potential():
    """Test potential scores endpoint."""
    r = client.get("/api/potential")
    assert r.status_code == 200


def test_competitiveness():
    """Test competitiveness endpoint."""
    r = client.get("/api/competitiveness")
    assert r.status_code == 200


def test_overview():
    """Test overview endpoint."""
    r = client.get("/api/overview")
    assert r.status_code == 200
    assert "total_sites" in r.json()


def test_drilldown():
    """Test city drilldown endpoint."""
    r = client.get("/api/drilldown/Bogota")
    assert r.status_code == 200
    assert r.json()["city"] == "Bogota"

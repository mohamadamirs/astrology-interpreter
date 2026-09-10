"""
API Endpoint Integration Tests (FEAT-01 QA)
Validates REST API contract, error handling, and dual-mode routing.
"""

import pytest
from starlette.testclient import TestClient
from backend.app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    """
    Verifies /health endpoint.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["precision_mode"] == "sub-arcsecond"


def test_calculate_chart_dual_mode():
    """
    FEAT-01: End-to-end Dual Mode calculation via REST API.
    """
    payload = {
        "latitude": -6.2088,
        "longitude": 106.8456,
        "local_datetime": "2000-01-01T12:00:00",
        "calculation_mode": "DUAL_MODE",
        "house_system": "WHOLE_SIGN",
        "ayanamsha": "LAHIRI"
    }
    response = client.post("/api/v1/charts/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    # Verify Geo resolution
    geo = data["resolved_geo"]
    assert geo["iana_timezone"] == "Asia/Jakarta"
    assert geo["utc_datetime_iso"] == "2000-01-01T05:00:00Z"

    # Verify Western chart payload exists
    west = data["western_chart"]
    assert west is not None
    assert west["zodiac_type"] == "TROPICAL"
    assert "SUN" in west["planets"]
    assert "angles" in west
    assert "aspects" in west

    # Verify Vedic chart payload exists
    vedic = data["vedic_chart"]
    assert vedic is not None
    assert vedic["zodiac_type"] == "SIDEREAL_LAHIRI"
    assert "MOON" in vedic["planets"]
    assert len(vedic["vimshottari_dasha_timeline"]) == 9


def test_calculate_chart_western_only():
    """
    FEAT-01: Western Only calculation mode omits Vedic payload.
    """
    payload = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "local_datetime": "2024-06-21T13:00:00",
        "calculation_mode": "WESTERN_ONLY",
        "house_system": "PLACIDUS"
    }
    response = client.post("/api/v1/charts/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["western_chart"] is not None
    assert data["vedic_chart"] is None


def test_calculate_chart_vedic_only():
    """
    FEAT-01: Vedic Only calculation mode omits Western payload.
    """
    payload = {
        "latitude": 35.6762,
        "longitude": 139.6503,
        "local_datetime": "2023-03-21T09:00:00",
        "calculation_mode": "VEDIC_ONLY"
    }
    response = client.post("/api/v1/charts/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()

    assert data["western_chart"] is None
    assert data["vedic_chart"] is not None


def test_invalid_coordinates_rejected():
    """
    Rejects invalid geographical coordinates with 422 Unprocessable Entity.
    """
    payload = {
        "latitude": 95.0,  # Invalid: > 90 deg
        "longitude": 106.8456,
        "local_datetime": "2000-01-01T12:00:00"
    }
    response = client.post("/api/v1/charts/calculate", json=payload)
    assert response.status_code == 422

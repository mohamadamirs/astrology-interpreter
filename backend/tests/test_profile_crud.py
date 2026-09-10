"""
Integration Tests for Profile Storage & Multi-Profile Management (FEAT-03 QA)
Validates full CRUD, offline caching, search, and soft-delete capabilities.
"""

import pytest
from starlette.testclient import TestClient
from backend.app.main import app
from backend.app.db.session import init_db

# Initialize database schema before tests
init_db()

client = TestClient(app)


def test_create_and_read_profile():
    """
    FEAT-03: Create a profile, verify precomputed caches, and retrieve by ID.
    """
    payload = {
        "profile_name": "Rian Pramana",
        "category": "SELF",
        "latitude": -6.175392,
        "longitude": 106.827153,
        "location_name": "Jakarta Pusat, DKI Jakarta",
        "local_datetime": "2000-01-01T12:00:00",
        "is_favorite": True
    }

    # 1. Create Profile
    res_create = client.post("/api/v1/chart/profiles", json=payload)
    assert res_create.status_code == 201
    data_create = res_create.json()["profile"]

    profile_id = data_create["id"]
    assert data_create["profile_name"] == "Rian Pramana"
    assert data_create["category"] == "SELF"
    assert data_create["iana_timezone"] == "Asia/Jakarta"
    assert data_create["is_favorite"] is True

    # Precomputed caches must exist
    assert data_create["cached_western"] is not None
    assert "SUN" in data_create["cached_western"]["planets"]
    assert data_create["cached_vedic"] is not None
    assert len(data_create["cached_vedic"]["vimshottari_dasha_timeline"]) == 9

    # 2. Retrieve Profile by ID
    res_get = client.get(f"/api/v1/chart/profiles/{profile_id}")
    assert res_get.status_code == 200
    data_get = res_get.json()["profile"]
    assert data_get["id"] == profile_id
    assert data_get["location_name"] == "Jakarta Pusat, DKI Jakarta"


def test_list_profiles_with_search_and_filter():
    """
    FEAT-03: List profiles with search query and category filtering.
    """
    # Create two distinct profiles
    client.post("/api/v1/chart/profiles", json={
        "profile_name": "Siti Rahma",
        "category": "FAMILY",
        "latitude": -6.9175,
        "longitude": 107.6191,
        "location_name": "Bandung, Jawa Barat",
        "local_datetime": "1998-05-15T08:30:00",
        "is_favorite": False
    })
    client.post("/api/v1/chart/profiles", json={
        "profile_name": "Budi Hartono",
        "category": "COWORKER",
        "latitude": -7.2575,
        "longitude": 112.7521,
        "location_name": "Surabaya, Jawa Timur",
        "local_datetime": "1995-11-20T14:15:00",
        "is_favorite": True
    })

    # Test Search by Query 'Rahma'
    res_search = client.get("/api/v1/chart/profiles?q=Rahma")
    assert res_search.status_code == 200
    search_data = res_search.json()
    assert search_data["total_count"] >= 1
    assert any("Siti Rahma" in p["profile_name"] for p in search_data["profiles"])

    # Test Filter by Category 'COWORKER'
    res_cat = client.get("/api/v1/chart/profiles?category=COWORKER")
    assert res_cat.status_code == 200
    cat_data = res_cat.json()
    assert all(p["category"] == "COWORKER" for p in cat_data["profiles"])

    # Test Filter by Favorite
    res_fav = client.get("/api/v1/chart/profiles?is_favorite=true")
    assert res_fav.status_code == 200
    fav_data = res_fav.json()
    assert all(p["is_favorite"] is True for p in fav_data["profiles"])


def test_update_profile_and_recomputation():
    """
    FEAT-03: Updating datetime triggers automatic cache recomputation.
    """
    # Create initial profile
    res_init = client.post("/api/v1/chart/profiles", json={
        "profile_name": "Eko Santoso",
        "category": "FRIEND",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "local_datetime": "2000-01-01T12:00:00"
    })
    pid = res_init.json()["profile"]["id"]
    initial_sun_lon = res_init.json()["profile"]["cached_western"]["planets"]["SUN"]["longitude"]

    # Update metadata only
    res_meta = client.put(f"/api/v1/chart/profiles/{pid}", json={
        "profile_name": "Eko Santoso M.T.",
        "is_favorite": True
    })
    assert res_meta.status_code == 200
    assert res_meta.json()["profile"]["profile_name"] == "Eko Santoso M.T."
    assert res_meta.json()["profile"]["is_favorite"] is True

    # Update birth datetime to 6 months later (July 1, 2000)
    # Sun will move ~180 degrees from Capricorn to Cancer
    res_recalc = client.put(f"/api/v1/chart/profiles/{pid}", json={
        "local_datetime": "2000-07-01T12:00:00"
    })
    assert res_recalc.status_code == 200
    updated_sun_lon = res_recalc.json()["profile"]["cached_western"]["planets"]["SUN"]["longitude"]

    # Verify that Sun position actually changed significantly
    assert abs(updated_sun_lon - initial_sun_lon) > 100.0


def test_soft_delete_profile():
    """
    FEAT-03: Soft-delete sets is_deleted=True and excludes from list and get queries.
    """
    res = client.post("/api/v1/chart/profiles", json={
        "profile_name": "Temporary Profile",
        "category": "OTHER",
        "latitude": -6.2088,
        "longitude": 106.8456,
        "local_datetime": "2000-01-01T12:00:00"
    })
    pid = res.json()["profile"]["id"]

    # Delete profile
    del_res = client.delete(f"/api/v1/chart/profiles/{pid}")
    assert del_res.status_code == 200

    # GET by ID must return 404
    get_res = client.get(f"/api/v1/chart/profiles/{pid}")
    assert get_res.status_code == 404

    # Profile must not appear in list
    list_res = client.get("/api/v1/chart/profiles?q=Temporary")
    assert list_res.status_code == 200
    assert all(p["id"] != pid for p in list_res.json()["profiles"])

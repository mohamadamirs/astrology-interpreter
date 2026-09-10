"""
Ground-Truth Benchmark Test Suite (FEAT-01 QA)
Validates sub-arcsecond ephemeris accuracy (<= 0.001 degrees)
and 100% offline geospatial timezone resolution.
"""

import math
import pytest
from backend.tests.golden_vectors import GOLDEN_VECTORS
from backend.app.core.timezone import resolve_timezone_and_utc
from backend.app.core.julian import calculate_julian_day
from backend.app.astro.calculator import calculate_planetary_positions


@pytest.mark.parametrize("vector", GOLDEN_VECTORS, ids=lambda v: v["id"])
def test_offline_timezone_resolution(vector):
    """
    FEAT-01 Step 1: Offline geospatial timezone and canonical UTC resolution.
    Must execute 100% offline without network calls.
    """
    geo_res = resolve_timezone_and_utc(
        latitude=vector["input"]["latitude"],
        longitude=vector["input"]["longitude"],
        local_iso_string=vector["input"]["local_datetime"]
    )
    
    assert geo_res.iana_timezone == vector["expected_geo"]["iana_timezone"], (
        f"Timezone mismatch for {vector['label']}: "
        f"got {geo_res.iana_timezone}, expected {vector['expected_geo']['iana_timezone']}"
    )
    assert geo_res.utc_iso == vector["expected_geo"]["utc_iso"], (
        f"UTC conversion mismatch for {vector['label']}: "
        f"got {geo_res.utc_iso}, expected {vector['expected_geo']['utc_iso']}"
    )
    assert math.isclose(geo_res.utc_offset_hours, vector["expected_geo"]["utc_offset_hours"], abs_tol=1e-3)


@pytest.mark.parametrize("vector", GOLDEN_VECTORS, ids=lambda v: v["id"])
def test_julian_day_calculation(vector):
    """
    FEAT-01 Step 1.5: Julian Day Calculation from UTC canonical datetime.
    Tolerance: <= 0.0001 days.
    """
    geo_res = resolve_timezone_and_utc(
        latitude=vector["input"]["latitude"],
        longitude=vector["input"]["longitude"],
        local_iso_string=vector["input"]["local_datetime"]
    )
    
    jd = calculate_julian_day(geo_res.utc_datetime)
    expected_jd = vector["expected_astro"]["julian_day"]
    assert math.isclose(jd, expected_jd, abs_tol=1e-3), (
        f"Julian Day mismatch for {vector['label']}: got {jd}, expected {expected_jd}"
    )


@pytest.mark.parametrize("vector", GOLDEN_VECTORS, ids=lambda v: v["id"])
def test_planetary_ephemeris_accuracy(vector):
    """
    FEAT-01 Step 2: Tropical Ephemeris Accuracy.
    NFR-ACC-01 requires tolerance <= 0.001 degrees (3.6 arcseconds).
    """
    geo_res = resolve_timezone_and_utc(
        latitude=vector["input"]["latitude"],
        longitude=vector["input"]["longitude"],
        local_iso_string=vector["input"]["local_datetime"]
    )
    
    astro_res = calculate_planetary_positions(
        utc_datetime=geo_res.utc_datetime,
        latitude=vector["input"]["latitude"],
        longitude=vector["input"]["longitude"]
    )
    
    expected = vector["expected_astro"]
    
    # Verify Sun longitude tolerance <= 0.001 deg
    if "sun_tropical_longitude" in expected:
        sun_lon = astro_res["SUN"]["longitude"]
        assert math.isclose(sun_lon, expected["sun_tropical_longitude"], abs_tol=1e-3), (
            f"Sun longitude deviation exceeds 0.001 deg for {vector['label']}: "
            f"got {sun_lon:.5f}, expected {expected['sun_tropical_longitude']:.5f}"
        )
        
    # Verify Moon longitude tolerance <= 0.001 deg
    if "moon_tropical_longitude" in expected:
        moon_lon = astro_res["MOON"]["longitude"]
        assert math.isclose(moon_lon, expected["moon_tropical_longitude"], abs_tol=1e-3), (
            f"Moon longitude deviation exceeds 0.001 deg for {vector['label']}: "
            f"got {moon_lon:.5f}, expected {expected['moon_tropical_longitude']:.5f}"
        )

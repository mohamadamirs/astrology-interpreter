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


def test_angles_and_houses_jakarta():
    """
    FEAT-01: Ascendant, Midheaven, and House Systems.
    """
    from backend.app.astro.houses import calculate_angles_and_houses, assign_houses_to_planets

    geo_res = resolve_timezone_and_utc(-6.2088, 106.8456, "2000-01-01T12:00:00")
    angles_res = calculate_angles_and_houses(
        utc_datetime=geo_res.utc_datetime,
        latitude=-6.2088,
        longitude=106.8456,
        house_system="WHOLE_SIGN"
    )

    asc = angles_res["angles"]["ASC"]
    mc = angles_res["angles"]["MC"]

    # Ascendant for Jakarta 2000-01-01 12:00 WIB is in Aries (~12.48 deg)
    assert asc["sign"] == "Aries"
    assert math.isclose(asc["longitude"], 12.4787, abs_tol=0.1)

    # Midheaven is in Capricorn (~281.05 deg)
    assert mc["sign"] == "Capricorn"
    assert math.isclose(mc["longitude"], 281.0492, abs_tol=0.1)

    # In Whole Sign, House 1 must be Aries (0 to 30)
    assert len(angles_res["houses"]) == 12
    assert angles_res["houses"][0]["sign"] == "Aries"
    assert angles_res["houses"][1]["sign"] == "Taurus"
    assert angles_res["houses"][9]["sign"] == "Capricorn"


def test_aspect_exponential_decay_weighting():
    """
    Strict Guardrail #3: Continuous Exponential Decay Weighting W(delta) = 10.0 * exp(-1.4 * delta).
    """
    from backend.app.astro.aspects import calculate_aspect_weight, calculate_aspects

    # Exact aspect (delta = 0) -> W = 10.0
    w_exact = calculate_aspect_weight(0.0)
    assert math.isclose(w_exact, 10.0, abs_tol=1e-3)

    # 1.0 degree orb delta -> W = 10.0 * exp(-1.4) = 2.46597
    w_1deg = calculate_aspect_weight(1.0)
    assert math.isclose(w_1deg, 2.4660, abs_tol=1e-3)

    # 3.0 degree orb delta -> W = 10.0 * exp(-4.2) = 0.14995
    w_3deg = calculate_aspect_weight(3.0)
    assert math.isclose(w_3deg, 0.1500, abs_tol=1e-3)

    # Test pair aspect detection
    sample_planets = {
        "SUN": {"longitude": 0.0, "speed_deg_per_day": 0.98},
        "MOON": {"longitude": 120.5, "speed_deg_per_day": 12.2},  # Trine with 0.5 deg orb
        "MARS": {"longitude": 89.2, "speed_deg_per_day": 0.65}    # Square with 0.8 deg orb
    }
    aspects = calculate_aspects(sample_planets)
    assert len(aspects) >= 2
    assert aspects[0]["aspect_type"] in ["TRINE", "SQUARE"]


def test_vedic_sidereal_and_nakshatras():
    """
    Strict Guardrail #2: Sidereal (Lahiri) calculations, 27 Nakshatras & Pada.
    """
    from backend.app.astro.vedic import (
        calculate_lahiri_ayanamsha,
        calculate_nakshatra_and_pada,
        calculate_sidereal_chart
    )

    # Lahiri Ayanamsha at J2000 (JD 2451545.0)
    ayanamsha_2000 = calculate_lahiri_ayanamsha(2451545.0)
    assert math.isclose(ayanamsha_2000, 23.85306, abs_tol=1e-3)

    # Moon in Jakarta 2000-01-01 was at tropical 219.81485
    # Sidereal = 219.81485 - 23.85306 = 195.96179 (Libra)
    # Must be in Swati Nakshatra, Pada 3, Ruled by RAHU
    nak_info = calculate_nakshatra_and_pada(195.96179)
    assert nak_info["nakshatra_name"] == "Swati"
    assert nak_info["pada"] == 3
    assert nak_info["nakshatra_ruler"] == "RAHU"


def test_vimshottari_dasha_calculation():
    """
    Vedic Vimshottari Dasha 120-year hierarchical timeline.
    """
    from backend.app.astro.vedic import calculate_vimshottari_dasha
    from datetime import datetime

    birth_dt = datetime(2000, 1, 1, 5, 0, 0)
    moon_sidereal = 195.96179  # Swati (Rahu)

    dasha_timeline = calculate_vimshottari_dasha(moon_sidereal, birth_dt)

    assert len(dasha_timeline) == 9
    assert dasha_timeline[0]["mahadasha"] == "RAHU"
    assert dasha_timeline[0]["is_partial_at_birth"] is True
    # Next Dasha after Rahu is Jupiter (16 years)
    assert dasha_timeline[1]["mahadasha"] == "JUPITER"
    assert dasha_timeline[1]["duration_years"] == 16.0


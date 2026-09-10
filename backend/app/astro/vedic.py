"""
Vedic / Sidereal Astrology Engine (FEAT-01)
Chitra Paksha (Lahiri) Ayanamsha, 27 Nakshatras, Pada, and Vimshottari Dasha Engine.
"""

from datetime import datetime, timedelta
import math
from typing import Dict, List, Any, Tuple

from backend.app.astro.calculator import ZODIAC_SIGNS
from backend.app.core.julian import calculate_julian_day

NAKSHATRAS = [
    {"name": "Ashwini", "ruler": "KETU"},
    {"name": "Bharani", "ruler": "VENUS"},
    {"name": "Krittika", "ruler": "SUN"},
    {"name": "Rohini", "ruler": "MOON"},
    {"name": "Mrigashira", "ruler": "MARS"},
    {"name": "Ardra", "ruler": "RAHU"},
    {"name": "Punarvasu", "ruler": "JUPITER"},
    {"name": "Pushya", "ruler": "SATURN"},
    {"name": "Ashlesha", "ruler": "MERCURY"},
    {"name": "Magha", "ruler": "KETU"},
    {"name": "Purva Phalguni", "ruler": "VENUS"},
    {"name": "Uttara Phalguni", "ruler": "SUN"},
    {"name": "Hasta", "ruler": "MOON"},
    {"name": "Chitra", "ruler": "MARS"},
    {"name": "Swati", "ruler": "RAHU"},
    {"name": "Vishakha", "ruler": "JUPITER"},
    {"name": "Anuradha", "ruler": "SATURN"},
    {"name": "Jyeshtha", "ruler": "MERCURY"},
    {"name": "Mula", "ruler": "KETU"},
    {"name": "Purva Ashadha", "ruler": "VENUS"},
    {"name": "Uttara Ashadha", "ruler": "SUN"},
    {"name": "Shravana", "ruler": "MOON"},
    {"name": "Dhanishta", "ruler": "MARS"},
    {"name": "Shatabhisha", "ruler": "RAHU"},
    {"name": "Purva Bhadrapada", "ruler": "JUPITER"},
    {"name": "Uttara Bhadrapada", "ruler": "SATURN"},
    {"name": "Revati", "ruler": "MERCURY"}
]

VIMSHOTTARI_YEARS = {
    "KETU": 7.0,
    "VENUS": 20.0,
    "SUN": 6.0,
    "MOON": 10.0,
    "MARS": 7.0,
    "RAHU": 18.0,
    "JUPITER": 16.0,
    "SATURN": 19.0,
    "MERCURY": 17.0
}

DASHA_SEQUENCE = ["KETU", "VENUS", "SUN", "MOON", "MARS", "RAHU", "JUPITER", "SATURN", "MERCURY"]


def calculate_lahiri_ayanamsha(jd: float) -> float:
    """
    Computes Lahiri (Chitra Paksha) Ayanamsha in degrees for a given Julian Day.
    Standard IAU precession calibrated for Lahiri epoch 2000.0.
    """
    t = (jd - 2451545.0) / 36525.0
    ayanamsha = 23.8530556 + 1.3969713 * t + 0.0003086 * (t**2)
    return ayanamsha


def calculate_nakshatra_and_pada(sidereal_longitude_deg: float) -> Dict[str, Any]:
    """
    Given a sidereal longitude [0, 360), computes the Nakshatra (1-27), Pada (1-4),
    Nakshatra Lord, and percentage progress.
    """
    nak_span = 360.0 / 27.0  # 13° 20' = 13.333333°
    pada_span = nak_span / 4.0  # 3° 20' = 3.333333°

    nak_index = int(sidereal_longitude_deg // nak_span) % 27
    nak_info = NAKSHATRAS[nak_index]

    rem_in_nak = sidereal_longitude_deg % nak_span
    pada = int(rem_in_nak // pada_span) + 1
    progress_ratio = rem_in_nak / nak_span

    return {
        "nakshatra_number": nak_index + 1,
        "nakshatra_name": nak_info["name"],
        "nakshatra_ruler": nak_info["ruler"],
        "pada": pada,
        "progress_percent": round(progress_ratio * 100.0, 2),
        "fraction_elapsed": progress_ratio
    }


def calculate_sidereal_chart(
    tropical_planets: Dict[str, Dict[str, Any]],
    utc_datetime: datetime
) -> Dict[str, Any]:
    """
    Converts tropical planetary positions into Sidereal positions via Lahiri Ayanamsha,
    computing Nakshatra and Pada for each planet.
    """
    jd = calculate_julian_day(utc_datetime)
    ayanamsha_deg = calculate_lahiri_ayanamsha(jd)

    sidereal_planets: Dict[str, Dict[str, Any]] = {}

    for name, p in tropical_planets.items():
        trop_lon = p["longitude"]
        sid_lon = (trop_lon - ayanamsha_deg) % 360.0

        s_idx = int(sid_lon // 30)
        nak_data = calculate_nakshatra_and_pada(sid_lon)

        sidereal_planets[name] = {
            "name": name,
            "longitude_sidereal": round(sid_lon, 6),
            "sign": ZODIAC_SIGNS[s_idx],
            "sign_index": s_idx + 1,
            "sign_degree": round(sid_lon % 30.0, 6),
            "is_retrograde": p.get("is_retrograde", False),
            "speed_deg_per_day": p.get("speed_deg_per_day", 0.0),
            "nakshatra": nak_data
        }

    return {
        "ayanamsha_type": "LAHIRI",
        "ayanamsha_degrees": round(ayanamsha_deg, 6),
        "planets": sidereal_planets
    }


def calculate_vimshottari_dasha(
    moon_sidereal_longitude: float,
    birth_utc_datetime: datetime,
    target_years_forward: int = 120
) -> List[Dict[str, Any]]:
    """
    Calculates the 120-year Vimshottari Mahadasha timeline starting from birth date.
    """
    nak_data = calculate_nakshatra_and_pada(moon_sidereal_longitude)
    start_ruler = nak_data["nakshatra_ruler"]
    frac_elapsed = nak_data["fraction_elapsed"]

    start_ruler_idx = DASHA_SEQUENCE.index(start_ruler)
    total_ruler_years = VIMSHOTTARI_YEARS[start_ruler]

    # Balance of first Mahadasha at birth
    remaining_first_dasha_years = total_ruler_years * (1.0 - frac_elapsed)

    timeline: List[Dict[str, Any]] = []
    current_date = birth_utc_datetime

    # 1. First Mahadasha (Partial)
    first_end = current_date + timedelta(days=remaining_first_dasha_years * 365.2425)
    timeline.append({
        "mahadasha": start_ruler,
        "duration_years": round(remaining_first_dasha_years, 3),
        "is_partial_at_birth": True,
        "start_date": current_date.strftime("%Y-%m-%d"),
        "end_date": first_end.strftime("%Y-%m-%d")
    })
    current_date = first_end

    # 2. Subsequent Mahadashas
    for k in range(1, 9):
        ruler_idx = (start_ruler_idx + k) % 9
        ruler_name = DASHA_SEQUENCE[ruler_idx]
        d_years = VIMSHOTTARI_YEARS[ruler_name]
        d_end = current_date + timedelta(days=d_years * 365.2425)

        timeline.append({
            "mahadasha": ruler_name,
            "duration_years": d_years,
            "is_partial_at_birth": False,
            "start_date": current_date.strftime("%Y-%m-%d"),
            "end_date": d_end.strftime("%Y-%m-%d")
        })
        current_date = d_end

    return timeline

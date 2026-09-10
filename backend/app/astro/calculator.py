"""
Astrological Planetary Positions Engine (FEAT-01)
High-precision ephemeris computation using PyEphem celestial mechanics.
"""

from datetime import datetime, timedelta
import math
from typing import Dict, Any

import ephem

ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

PLANET_FACTORIES = {
    "SUN": ephem.Sun,
    "MOON": ephem.Moon,
    "MERCURY": ephem.Mercury,
    "VENUS": ephem.Venus,
    "MARS": ephem.Mars,
    "JUPITER": ephem.Jupiter,
    "SATURN": ephem.Saturn,
    "URANUS": ephem.Uranus,
    "NEPTUNE": ephem.Neptune,
    "PLUTO": ephem.Pluto,
}


def calculate_planetary_positions(
    utc_datetime: datetime,
    latitude: float,
    longitude: float
) -> Dict[str, Dict[str, Any]]:
    """
    Computes sub-arcsecond tropical ecliptic longitudes, speeds,
    zodiac sign placements, and retrograde flags for the 10 planetary bodies.
    """
    date_str = utc_datetime.strftime("%Y/%m/%d %H:%M:%S")
    ephem_date = ephem.Date(date_str)
    
    # Observer setup
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.elevation = 0
    observer.date = ephem_date

    # Micro-offset for speed/retrograde calculation (1 hour differential)
    dt_forward = utc_datetime + timedelta(hours=1)
    ephem_date_forward = ephem.Date(dt_forward.strftime("%Y/%m/%d %H:%M:%S"))

    results: Dict[str, Dict[str, Any]] = {}

    for name, factory in PLANET_FACTORIES.items():
        body = factory()
        body.compute(ephem_date)
        ecl = ephem.Ecliptic(body)
        lon_deg = math.degrees(ecl.lon) % 360.0
        lat_deg = math.degrees(ecl.lat)

        # Compute speed over 1 hour to detect retrograde motion
        body_next = factory()
        body_next.compute(ephem_date_forward)
        lon_next = math.degrees(ephem.Ecliptic(body_next).lon) % 360.0

        # Handle circular wrap-around at 0/360 boundary
        delta_deg = lon_next - lon_deg
        if delta_deg > 180.0:
            delta_deg -= 360.0
        elif delta_deg < -180.0:
            delta_deg += 360.0

        speed_deg_per_day = delta_deg * 24.0
        is_retrograde = speed_deg_per_day < 0.0

        sign_index = int(lon_deg // 30)
        sign_name = ZODIAC_SIGNS[sign_index]
        sign_degree = lon_deg % 30.0

        results[name] = {
            "name": name,
            "longitude": round(lon_deg, 6),
            "ecliptic_latitude": round(lat_deg, 6),
            "sign": sign_name,
            "sign_index": sign_index + 1,  # 1-indexed (1=Aries, 12=Pisces)
            "sign_degree": round(sign_degree, 6),
            "speed_deg_per_day": round(speed_deg_per_day, 6),
            "is_retrograde": is_retrograde,
        }

    return results

"""
Astronomical Julian Day & Sidereal Time Calculations (FEAT-01)
Deterministic mathematical algorithms based on standard IAU celestial mechanics.
"""

import math
from datetime import datetime


def calculate_julian_day(utc_dt: datetime) -> float:
    """
    Calculates the exact Julian Day (JD) for a given UTC datetime.
    Formula: Meeus Astronomical Algorithms (Chapter 7).
    """
    year = utc_dt.year
    month = utc_dt.month
    day = utc_dt.day

    # Decimal fraction of the day in UTC
    ut = utc_dt.hour + (utc_dt.minute / 60.0) + (utc_dt.second + utc_dt.microsecond / 1e6) / 3600.0

    if month <= 2:
        year -= 1
        month += 12

    # Gregorian calendar reform adjustment
    a = math.floor(year / 100.0)
    b = 2 - a + math.floor(a / 4.0)

    jd = (
        math.floor(365.25 * (year + 4716))
        + math.floor(30.6001 * (month + 1))
        + day
        + b
        - 1524.5
        + (ut / 24.0)
    )
    return jd


def calculate_gmst(jd: float) -> float:
    """
    Computes Greenwich Mean Sidereal Time (GMST) in degrees [0, 360).
    """
    t = (jd - 2451545.0) / 36525.0
    gmst = (
        280.46061837
        + 360.98564736629 * (jd - 2451545.0)
        + 0.000387933 * (t**2)
        - (t**3) / 38710000.0
    )
    return gmst % 360.0


def calculate_local_sidereal_time(gmst_deg: float, longitude_deg: float) -> float:
    """
    Computes Local Sidereal Time (LST / RAMC) in degrees [0, 360).
    """
    return (gmst_deg + longitude_deg) % 360.0

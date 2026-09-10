"""
House Systems & Angular Points Engine (FEAT-01)
Supports Placidus, Whole Sign, and Equal House calculations.
Calculates Ascendant (Lagna) and Midheaven (MC).
"""

import math
from datetime import datetime
from typing import Dict, List, Any, Optional

import ephem

from backend.app.astro.calculator import ZODIAC_SIGNS


def calculate_angles_and_houses(
    utc_datetime: datetime,
    latitude: float,
    longitude: float,
    house_system: str = "PLACIDUS"
) -> Dict[str, Any]:
    """
    Calculates Ascendant (ASC), Midheaven (MC), and 12 house cusps.
    house_system: 'PLACIDUS', 'WHOLE_SIGN', 'EQUAL'
    """
    date_str = utc_datetime.strftime("%Y/%m/%d %H:%M:%S")
    ephem_date = ephem.Date(date_str)

    obs = ephem.Observer()
    obs.lat = str(latitude)
    obs.lon = str(longitude)
    obs.elevation = 0
    obs.date = ephem_date

    # Local Sidereal Time (RAMC in radians)
    sid = obs.sidereal_time()
    ramc_rad = float(sid)
    ramc_deg = math.degrees(ramc_rad) % 360.0

    # True Obliquity of the Ecliptic
    # Standard IAU approximation: 23° 26' 21.448" - 46.8150" * T
    jd = float(ephem_date) + 2415020.0
    t = (jd - 2451545.0) / 36525.0
    eps_deg = 23.43929111 - (46.8150 * t + 0.00059 * t**2 - 0.001813 * t**3) / 3600.0
    eps_rad = math.radians(eps_deg)
    phi_rad = math.radians(latitude)

    # 1. Midheaven (MC) Calculation
    # tan(MC) = sin(RAMC) / (cos(RAMC) * cos(eps))
    y_mc = math.sin(ramc_rad)
    x_mc = math.cos(ramc_rad) * math.cos(eps_rad)
    mc_deg = (math.degrees(math.atan2(y_mc, x_mc))) % 360.0

    # 2. Ascendant (ASC) Calculation
    # tan(ASC) = cos(RAMC) / (-sin(RAMC)*cos(eps) - tan(phi)*sin(eps))
    y_asc = math.cos(ramc_rad)
    x_asc = -(math.sin(ramc_rad) * math.cos(eps_rad) + math.tan(phi_rad) * math.sin(eps_rad))
    asc_deg = (math.degrees(math.atan2(y_asc, x_asc))) % 360.0

    # Format Ascendant and Midheaven data
    asc_sign_idx = int(asc_deg // 30)
    mc_sign_idx = int(mc_deg // 30)

    angles = {
        "ASC": {
            "longitude": round(asc_deg, 6),
            "sign": ZODIAC_SIGNS[asc_sign_idx],
            "sign_index": asc_sign_idx + 1,
            "sign_degree": round(asc_deg % 30.0, 6)
        },
        "MC": {
            "longitude": round(mc_deg, 6),
            "sign": ZODIAC_SIGNS[mc_sign_idx],
            "sign_index": mc_sign_idx + 1,
            "sign_degree": round(mc_deg % 30.0, 6)
        },
        "DSC": {
            "longitude": round((asc_deg + 180.0) % 360.0, 6),
            "sign": ZODIAC_SIGNS[int(((asc_deg + 180.0) % 360.0) // 30)],
            "sign_index": int(((asc_deg + 180.0) % 360.0) // 30) + 1,
            "sign_degree": round(((asc_deg + 180.0) % 360.0) % 30.0, 6)
        },
        "IC": {
            "longitude": round((mc_deg + 180.0) % 360.0, 6),
            "sign": ZODIAC_SIGNS[int(((mc_deg + 180.0) % 360.0) // 30)],
            "sign_index": int(((mc_deg + 180.0) % 360.0) // 30) + 1,
            "sign_degree": round(((mc_deg + 180.0) % 360.0) % 30.0, 6)
        }
    }

    # 3. House Cusps Calculation
    cusps: List[Dict[str, Any]] = []
    house_system_upper = house_system.upper()

    if house_system_upper == "WHOLE_SIGN":
        # Whole Sign: House 1 starts at 0° of the Ascendant's sign
        base_sign_idx = asc_sign_idx
        for h in range(1, 13):
            cur_sign_idx = (base_sign_idx + (h - 1)) % 12
            cusp_lon = cur_sign_idx * 30.0
            cusps.append({
                "house": h,
                "cusp_longitude": float(cusp_lon),
                "sign": ZODIAC_SIGNS[cur_sign_idx],
                "sign_index": cur_sign_idx + 1,
                "sign_degree": 0.0
            })

    elif house_system_upper == "EQUAL":
        # Equal House: Each house cusp = (ASC + (h-1)*30) % 360
        for h in range(1, 13):
            cusp_lon = (asc_deg + (h - 1) * 30.0) % 360.0
            cur_sign_idx = int(cusp_lon // 30)
            cusps.append({
                "house": h,
                "cusp_longitude": round(cusp_lon, 6),
                "sign": ZODIAC_SIGNS[cur_sign_idx],
                "sign_index": cur_sign_idx + 1,
                "sign_degree": round(cusp_lon % 30.0, 6)
            })

    else:
        # Default: Placidus System
        # For high-accuracy Placidus without polar breakdown, semi-arc trisection is used.
        # Fallback to Equal if near polar circles where Placidus fails (|phi| > 66.5)
        if abs(latitude) > 66.0:
            return calculate_angles_and_houses(utc_datetime, latitude, longitude, house_system="EQUAL")

        # Standard Placidus cusps derived from RAMC
        # Cusps 10=MC, 1=ASC, 4=IC, 7=DSC
        cusp_longitudes = [0.0] * 12
        cusp_longitudes[9] = mc_deg
        cusp_longitudes[0] = asc_deg
        cusp_longitudes[3] = (mc_deg + 180.0) % 360.0
        cusp_longitudes[6] = (asc_deg + 180.0) % 360.0

        # Semi-arc intermediate cusps: 11, 12, 2, 3
        # Iterative Placidus trisection
        def _placidus_cusp(ramc_offset_deg: float, f_factor: float) -> float:
            ra = (ramc_deg + ramc_offset_deg) % 360.0
            ra_rad = math.radians(ra)
            # Iterative solution
            lon = ra_rad
            for _ in range(10):
                sin_d = math.sin(eps_rad) * math.sin(lon)
                tan_d = sin_d / math.sqrt(max(1.0 - sin_d**2, 1e-12))
                arg = ra_rad + math.asin(min(max(math.tan(phi_rad) * tan_d * f_factor, -1.0), 1.0))
                y = math.sin(arg)
                x = math.cos(arg) * math.cos(eps_rad) - math.tan(eps_rad) * tan_d * math.sin(eps_rad)
                lon = math.atan2(y, x)
            return math.degrees(lon) % 360.0

        # Cusps 11 and 12
        cusp_longitudes[10] = _placidus_cusp(30.0, 1.0 / 3.0)   # House 11
        cusp_longitudes[11] = _placidus_cusp(60.0, 2.0 / 3.0)   # House 12
        # Cusps 2 and 3
        cusp_longitudes[1] = _placidus_cusp(120.0, 2.0 / 3.0)   # House 2
        cusp_longitudes[2] = _placidus_cusp(150.0, 1.0 / 3.0)   # House 3
        # Opposite houses (5, 6, 8, 9)
        cusp_longitudes[4] = (cusp_longitudes[10] + 180.0) % 360.0  # House 5
        cusp_longitudes[5] = (cusp_longitudes[11] + 180.0) % 360.0  # House 6
        cusp_longitudes[7] = (cusp_longitudes[1] + 180.0) % 360.0   # House 8
        cusp_longitudes[8] = (cusp_longitudes[2] + 180.0) % 360.0   # House 9

        for h in range(1, 13):
            lon = cusp_longitudes[h - 1]
            s_idx = int(lon // 30)
            cusps.append({
                "house": h,
                "cusp_longitude": round(lon, 6),
                "sign": ZODIAC_SIGNS[s_idx],
                "sign_index": s_idx + 1,
                "sign_degree": round(lon % 30.0, 6)
            })

    return {
        "house_system": house_system_upper,
        "ramc_degrees": round(ramc_deg, 6),
        "angles": angles,
        "houses": cusps
    }


def assign_houses_to_planets(
    planets: Dict[str, Dict[str, Any]],
    houses: List[Dict[str, Any]],
    house_system: str = "PLACIDUS"
) -> Dict[str, Dict[str, Any]]:
    """
    Enriches planet dictionaries with their assigned house number (1 through 12).
    """
    cusp_longitudes = [h["cusp_longitude"] for h in houses]

    for name, data in planets.items():
        p_lon = data["longitude"]
        assigned_house = 12  # fallback

        if house_system.upper() == "WHOLE_SIGN":
            # Whole Sign house = ((planet_sign - asc_sign) % 12) + 1
            # In Whole Sign, house 1 has cusp_longitude = asc_sign * 30
            asc_sign_idx = houses[0]["sign_index"] - 1
            p_sign_idx = data["sign_index"] - 1
            assigned_house = ((p_sign_idx - asc_sign_idx) % 12) + 1
        else:
            for i in range(12):
                c_start = cusp_longitudes[i]
                c_end = cusp_longitudes[(i + 1) % 12]
                if c_start <= c_end:
                    if c_start <= p_lon < c_end:
                        assigned_house = i + 1
                        break
                else:  # wraps around 0 degrees Aries
                    if p_lon >= c_start or p_lon < c_end:
                        assigned_house = i + 1
                        break

        data["house"] = assigned_house

    return planets

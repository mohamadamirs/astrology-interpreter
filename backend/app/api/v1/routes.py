"""
API v1 Routes for Chart Calculations (FEAT-01)
"""

from fastapi import APIRouter, HTTPException, status
from backend.app.models.schemas import (
    ChartCalculationRequest,
    ChartCalculationResponse,
    CalculationMode,
    GeoResolution
)
from backend.app.core.timezone import resolve_timezone_and_utc
from backend.app.core.julian import calculate_julian_day
from backend.app.astro.calculator import calculate_planetary_positions
from backend.app.astro.houses import calculate_angles_and_houses, assign_houses_to_planets
from backend.app.astro.aspects import calculate_aspects
from backend.app.astro.vedic import (
    calculate_sidereal_chart,
    calculate_vimshottari_dasha
)

router = APIRouter(prefix="/charts", tags=["charts"])


@router.post(
    "/calculate",
    response_model=ChartCalculationResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate Flexible Birth Chart (Western, Vedic, or Both)"
)
async def calculate_chart(req: ChartCalculationRequest):
    """
    Computes deterministic celestial positions, houses, aspects,
    and Vedic Dasha hierarchies based on physical coordinates.
    """
    try:
        # 1. Resolve offline timezone and UTC
        geo = resolve_timezone_and_utc(
            latitude=req.latitude,
            longitude=req.longitude,
            local_iso_string=req.local_datetime
        )
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(err)
        )
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Timezone resolution failed: {str(err)}"
        )

    jd = calculate_julian_day(geo.utc_datetime)

    geo_resolution = GeoResolution(
        latitude=geo.latitude,
        longitude=geo.longitude,
        iana_timezone=geo.iana_timezone,
        local_datetime_iso=geo.local_datetime.isoformat(),
        utc_datetime_iso=geo.utc_iso,
        utc_offset_hours=geo.utc_offset_hours,
        julian_day=round(jd, 6)
    )

    # 2. Compute base planetary coordinates
    tropical_planets = calculate_planetary_positions(
        utc_datetime=geo.utc_datetime,
        latitude=req.latitude,
        longitude=req.longitude
    )

    western_payload = None
    vedic_payload = None

    # 3. Western Calculation Pipeline
    if req.calculation_mode in [CalculationMode.WESTERN_ONLY, CalculationMode.DUAL_MODE]:
        angles_houses = calculate_angles_and_houses(
            utc_datetime=geo.utc_datetime,
            latitude=req.latitude,
            longitude=req.longitude,
            house_system=req.house_system.value
        )
        planets_with_houses = assign_houses_to_planets(
            planets=tropical_planets,
            houses=angles_houses["houses"],
            house_system=req.house_system.value
        )
        active_aspects = calculate_aspects(planets_with_houses)

        western_payload = {
            "zodiac_type": "TROPICAL",
            "house_system": req.house_system.value,
            "angles": angles_houses["angles"],
            "houses": angles_houses["houses"],
            "planets": planets_with_houses,
            "aspects": active_aspects
        }

    # 4. Vedic Calculation Pipeline
    if req.calculation_mode in [CalculationMode.VEDIC_ONLY, CalculationMode.DUAL_MODE]:
        sidereal_data = calculate_sidereal_chart(
            tropical_planets=tropical_planets,
            utc_datetime=geo.utc_datetime
        )
        moon_sid_lon = sidereal_data["planets"]["MOON"]["longitude_sidereal"]
        dasha_timeline = calculate_vimshottari_dasha(
            moon_sidereal_longitude=moon_sid_lon,
            birth_utc_datetime=geo.utc_datetime
        )

        vedic_payload = {
            "zodiac_type": "SIDEREAL_LAHIRI",
            "ayanamsha": sidereal_data["ayanamsha_degrees"],
            "planets": sidereal_data["planets"],
            "vimshottari_dasha_timeline": dasha_timeline
        }

    return ChartCalculationResponse(
        status="success",
        calculation_mode=req.calculation_mode,
        resolved_geo=geo_resolution,
        western_chart=western_payload,
        vedic_chart=vedic_payload
    )

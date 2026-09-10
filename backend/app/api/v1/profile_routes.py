"""
Profile Storage Management Routes (FEAT-03)
Implements Create, Read, Update, and Soft-Delete operations for multi-user charts.
"""

from typing import Optional, List, Tuple, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, func

from backend.app.db.session import get_db
from backend.app.db.models import SavedChart
from backend.app.models.profile_schemas import (
    ProfileCreate,
    ProfileUpdate,
    ProfileCategory,
    ProfileSummary,
    ProfileDetail,
    ProfileListResponse,
    ProfileSingleResponse
)
from backend.app.core.timezone import resolve_timezone_and_utc
from backend.app.core.julian import calculate_julian_day
from backend.app.astro.calculator import calculate_planetary_positions
from backend.app.astro.houses import calculate_angles_and_houses, assign_houses_to_planets
from backend.app.astro.aspects import calculate_aspects
from backend.app.astro.vedic import calculate_sidereal_chart, calculate_vimshottari_dasha

router = APIRouter(prefix="/chart/profiles", tags=["profile-storage"])


def _compute_full_chart_cache(
    latitude: float,
    longitude: float,
    local_datetime_str: str
) -> Tuple[Any, float, Dict[str, Any], Dict[str, Any], str, str, str]:
    """
    Computes and packages both Western and Vedic calculations for permanent caching.
    """
    geo = resolve_timezone_and_utc(latitude, longitude, local_datetime_str)
    jd = calculate_julian_day(geo.utc_datetime)

    # 1. Base planetary calculation
    tropical_planets = calculate_planetary_positions(geo.utc_datetime, latitude, longitude)

    # 2. Western chart
    angles_houses = calculate_angles_and_houses(
        utc_datetime=geo.utc_datetime,
        latitude=latitude,
        longitude=longitude,
        house_system="PLACIDUS"
    )
    planets_with_houses = assign_houses_to_planets(
        planets=tropical_planets,
        houses=angles_houses["houses"],
        house_system="PLACIDUS"
    )
    aspects = calculate_aspects(planets_with_houses)

    western_payload = {
        "zodiac_type": "TROPICAL",
        "house_system": "PLACIDUS",
        "angles": angles_houses["angles"],
        "houses": angles_houses["houses"],
        "planets": planets_with_houses,
        "aspects": aspects
    }

    # 3. Vedic chart
    sidereal_data = calculate_sidereal_chart(tropical_planets, geo.utc_datetime)
    moon_sid_lon = sidereal_data["planets"]["MOON"]["longitude_sidereal"]
    dasha = calculate_vimshottari_dasha(moon_sid_lon, geo.utc_datetime)

    vedic_payload = {
        "zodiac_type": "SIDEREAL_LAHIRI",
        "ayanamsha": sidereal_data["ayanamsha_degrees"],
        "planets": sidereal_data["planets"],
        "vimshottari_dasha_timeline": dasha
    }

    sun_sign = tropical_planets["SUN"]["sign"]
    moon_sign = tropical_planets["MOON"]["sign"]
    asc_sign = angles_houses["angles"]["ASC"]["sign"]

    return geo, jd, western_payload, vedic_payload, sun_sign, moon_sign, asc_sign


@router.post(
    "",
    response_model=ProfileSingleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create and Store New Birth Profile"
)
async def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)):
    """
    Stores birth coordinates and automatically pre-computes celestial caches.
    """
    try:
        geo, jd, west_cache, vedic_cache, _, _, _ = _compute_full_chart_cache(
            latitude=payload.latitude,
            longitude=payload.longitude,
            local_datetime_str=payload.local_datetime
        )
    except ValueError as err:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Computation failed: {str(err)}")

    new_chart = SavedChart(
        profile_name=payload.profile_name,
        category=payload.category.value,
        latitude=payload.latitude,
        longitude=payload.longitude,
        location_name=payload.location_name,
        local_datetime=payload.local_datetime,
        iana_timezone=geo.iana_timezone,
        utc_timestamp=geo.utc_iso,
        julian_day=jd,
        cached_western=west_cache,
        cached_vedic=vedic_cache,
        is_favorite=payload.is_favorite
    )

    db.add(new_chart)
    db.commit()
    db.refresh(new_chart)

    return ProfileSingleResponse(
        profile=ProfileDetail(
            id=new_chart.id,
            profile_name=new_chart.profile_name,
            category=new_chart.category,
            latitude=new_chart.latitude,
            longitude=new_chart.longitude,
            location_name=new_chart.location_name,
            local_datetime=new_chart.local_datetime,
            iana_timezone=new_chart.iana_timezone,
            utc_timestamp=new_chart.utc_timestamp,
            julian_day=new_chart.julian_day,
            is_favorite=new_chart.is_favorite,
            cached_western=new_chart.cached_western,
            cached_vedic=new_chart.cached_vedic,
            created_at=new_chart.created_at.isoformat(),
            updated_at=new_chart.updated_at.isoformat()
        )
    )


@router.get(
    "",
    response_model=ProfileListResponse,
    status_code=status.HTTP_200_OK,
    summary="List Stored Profiles with Filtering and Search"
)
async def list_profiles(
    q: Optional[str] = Query(default=None, description="Search profile name or location"),
    category: Optional[ProfileCategory] = Query(default=None, description="Filter by category"),
    is_favorite: Optional[bool] = Query(default=None, description="Filter by favorite bookmark"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retrieves stored profiles matching query parameters.
    """
    query = select(SavedChart).where(SavedChart.is_deleted.is_(False))

    if q:
        search_pattern = f"%{q.strip()}%"
        query = query.where(
            (SavedChart.profile_name.ilike(search_pattern)) |
            (SavedChart.location_name.ilike(search_pattern))
        )
    if category:
        query = query.where(SavedChart.category == category.value)
    if is_favorite is not None:
        query = query.where(SavedChart.is_favorite.is_(is_favorite))

    # Total count
    count_stmt = select(func.count()).select_from(query.subquery())
    total_count = db.scalar(count_stmt) or 0

    # Paging
    query = query.order_by(SavedChart.is_favorite.desc(), SavedChart.updated_at.desc())
    query = query.limit(limit).offset(offset)
    records = db.scalars(query).all()

    summaries: List[ProfileSummary] = []
    for r in records:
        sun_sign = None
        moon_sign = None
        asc_sign = None

        if r.cached_western and "planets" in r.cached_western:
            sun_sign = r.cached_western["planets"].get("SUN", {}).get("sign")
            moon_sign = r.cached_western["planets"].get("MOON", {}).get("sign")
            asc_sign = r.cached_western.get("angles", {}).get("ASC", {}).get("sign")

        summaries.append(ProfileSummary(
            id=r.id,
            profile_name=r.profile_name,
            category=r.category,
            location_name=r.location_name,
            local_datetime=r.local_datetime,
            iana_timezone=r.iana_timezone,
            sun_sign=sun_sign,
            moon_sign=moon_sign,
            ascendant_sign=asc_sign,
            is_favorite=r.is_favorite,
            created_at=r.created_at.isoformat(),
            updated_at=r.updated_at.isoformat()
        ))

    return ProfileListResponse(total_count=total_count, profiles=summaries)


@router.get(
    "/{profile_id}",
    response_model=ProfileSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Single Profile Detail with Full Cached Charts"
)
async def get_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Retrieves full profile data including precomputed Western and Vedic charts.
    """
    stmt = select(SavedChart).where(SavedChart.id == profile_id, SavedChart.is_deleted.is_(False))
    chart = db.scalar(stmt)
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    return ProfileSingleResponse(
        profile=ProfileDetail(
            id=chart.id,
            profile_name=chart.profile_name,
            category=chart.category,
            latitude=chart.latitude,
            longitude=chart.longitude,
            location_name=chart.location_name,
            local_datetime=chart.local_datetime,
            iana_timezone=chart.iana_timezone,
            utc_timestamp=chart.utc_timestamp,
            julian_day=chart.julian_day,
            is_favorite=chart.is_favorite,
            cached_western=chart.cached_western,
            cached_vedic=chart.cached_vedic,
            created_at=chart.created_at.isoformat(),
            updated_at=chart.updated_at.isoformat()
        )
    )


@router.put(
    "/{profile_id}",
    response_model=ProfileSingleResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Profile Metadata or Recalculate if Coordinates/Time Change"
)
async def update_profile(
    profile_id: str,
    payload: ProfileUpdate,
    db: Session = Depends(get_db)
):
    """
    Updates profile fields. If coordinates or datetime change, recalculates cached charts.
    """
    stmt = select(SavedChart).where(SavedChart.id == profile_id, SavedChart.is_deleted.is_(False))
    chart = db.scalar(stmt)
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    # Check if astronomical inputs changed
    new_lat = payload.latitude if payload.latitude is not None else chart.latitude
    new_lon = payload.longitude if payload.longitude is not None else chart.longitude
    new_dt = payload.local_datetime if payload.local_datetime is not None else chart.local_datetime

    inputs_changed = (
        new_lat != chart.latitude or
        new_lon != chart.longitude or
        new_dt != chart.local_datetime
    )

    if inputs_changed:
        geo, jd, west_cache, vedic_cache, _, _, _ = _compute_full_chart_cache(
            latitude=new_lat,
            longitude=new_lon,
            local_datetime_str=new_dt
        )
        chart.latitude = new_lat
        chart.longitude = new_lon
        chart.local_datetime = new_dt
        chart.iana_timezone = geo.iana_timezone
        chart.utc_timestamp = geo.utc_iso
        chart.julian_day = jd
        chart.cached_western = west_cache
        chart.cached_vedic = vedic_cache

    if payload.profile_name is not None:
        chart.profile_name = payload.profile_name
    if payload.category is not None:
        chart.category = payload.category.value
    if payload.location_name is not None:
        chart.location_name = payload.location_name
    if payload.is_favorite is not None:
        chart.is_favorite = payload.is_favorite

    db.commit()
    db.refresh(chart)

    return ProfileSingleResponse(
        profile=ProfileDetail(
            id=chart.id,
            profile_name=chart.profile_name,
            category=chart.category,
            latitude=chart.latitude,
            longitude=chart.longitude,
            location_name=chart.location_name,
            local_datetime=chart.local_datetime,
            iana_timezone=chart.iana_timezone,
            utc_timestamp=chart.utc_timestamp,
            julian_day=chart.julian_day,
            is_favorite=chart.is_favorite,
            cached_western=chart.cached_western,
            cached_vedic=chart.cached_vedic,
            created_at=chart.created_at.isoformat(),
            updated_at=chart.updated_at.isoformat()
        )
    )


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_200_OK,
    summary="Soft-Delete Profile"
)
async def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    """
    Soft-deletes a profile by setting is_deleted=True.
    """
    stmt = select(SavedChart).where(SavedChart.id == profile_id, SavedChart.is_deleted.is_(False))
    chart = db.scalar(stmt)
    if not chart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")

    chart.is_deleted = True
    db.commit()

    return {"status": "success", "message": f"Profile {profile_id} successfully deleted"}

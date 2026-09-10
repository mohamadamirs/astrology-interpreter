"""
Geospatial Timezone & Canonical UTC Resolution Module (FEAT-01)
100% Offline via TimezoneFinder polygon queries and standard zoneinfo.
"""

from dataclasses import dataclass
from datetime import datetime
import zoneinfo
from timezonefinder import TimezoneFinder

# Singleton instance to avoid reloading spatial polygons on every request
_TF_INSTANCE = TimezoneFinder()


@dataclass(frozen=True)
class TimezoneResult:
    latitude: float
    longitude: float
    iana_timezone: str
    local_datetime: datetime
    utc_datetime: datetime
    utc_iso: str
    utc_offset_hours: float


def resolve_timezone_and_utc(
    latitude: float,
    longitude: float,
    local_iso_string: str
) -> TimezoneResult:
    """
    Resolves local civil datetime and physical coordinates into an IANA timezone
    and exact canonical UTC datetime with zero internet dependency.
    """
    if not (-90.0 <= latitude <= 90.0):
        raise ValueError(f"Latitude {latitude} is outside valid range [-90.0, +90.0]")
    if not (-180.0 <= longitude <= 180.0):
        raise ValueError(f"Longitude {longitude} is outside valid range [-180.0, +180.0]")

    # 1. Query offline spatial polygons
    iana_name = _TF_INSTANCE.timezone_at(lat=latitude, lng=longitude)
    if not iana_name:
        # Fallback for international waters / maritime coordinates based on longitude
        estimated_offset = round(longitude / 15.0)
        iana_name = f"Etc/GMT{-estimated_offset:+d}" if estimated_offset != 0 else "UTC"

    # 2. Parse ISO-8601 string
    # Supports formats with or without seconds: YYYY-MM-DDTHH:MM[:SS]
    clean_iso = local_iso_string.strip()
    if len(clean_iso) == 16:  # YYYY-MM-DDTHH:MM
        clean_iso += ":00"

    naive_dt = datetime.fromisoformat(clean_iso)

    # 3. Bind zoneinfo timezone and convert to UTC
    tz = zoneinfo.ZoneInfo(iana_name)
    local_dt = naive_dt.replace(tzinfo=tz)
    utc_dt = local_dt.astimezone(zoneinfo.ZoneInfo("UTC"))

    # 4. Compute UTC offset in hours
    offset = local_dt.utcoffset()
    offset_hours = offset.total_seconds() / 3600.0 if offset else 0.0

    # 5. Format canonical UTC ISO string
    utc_iso = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    return TimezoneResult(
        latitude=latitude,
        longitude=longitude,
        iana_timezone=iana_name,
        local_datetime=local_dt,
        utc_datetime=utc_dt,
        utc_iso=utc_iso,
        utc_offset_hours=offset_hours
    )

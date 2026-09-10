"""
Pydantic Schemas for Chart Calculation Engine (FEAT-01)
Strict input validation and response contracts.
"""

from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class CalculationMode(str, Enum):
    WESTERN_ONLY = "WESTERN_ONLY"
    VEDIC_ONLY = "VEDIC_ONLY"
    DUAL_MODE = "DUAL_MODE"


class HouseSystem(str, Enum):
    PLACIDUS = "PLACIDUS"
    WHOLE_SIGN = "WHOLE_SIGN"
    EQUAL = "EQUAL"


class Ayanamsha(str, Enum):
    LAHIRI = "LAHIRI"
    KP = "KP"
    RAMAN = "RAMAN"


class ChartCalculationRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Longitude in decimal degrees")
    local_datetime: str = Field(..., description="Local civil birth datetime in ISO-8601 format (YYYY-MM-DDTHH:MM:SS)")
    calculation_mode: CalculationMode = Field(default=CalculationMode.DUAL_MODE, description="Calculation paradigm")
    house_system: HouseSystem = Field(default=HouseSystem.PLACIDUS, description="Western house system")
    ayanamsha: Ayanamsha = Field(default=Ayanamsha.LAHIRI, description="Sidereal ayanamsha")


class GeoResolution(BaseModel):
    latitude: float
    longitude: float
    iana_timezone: str
    local_datetime_iso: str
    utc_datetime_iso: str
    utc_offset_hours: float
    julian_day: float


class ChartCalculationResponse(BaseModel):
    status: str = "success"
    calculation_mode: CalculationMode
    resolved_geo: GeoResolution
    western_chart: Optional[Dict[str, Any]] = None
    vedic_chart: Optional[Dict[str, Any]] = None

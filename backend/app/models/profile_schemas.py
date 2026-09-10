"""
Pydantic Schemas for Profile Storage Management (FEAT-03)
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class ProfileCategory(str, Enum):
    SELF = "SELF"
    FAMILY = "FAMILY"
    FRIEND = "FRIEND"
    COWORKER = "COWORKER"
    PARTNER = "PARTNER"
    OTHER = "OTHER"


class ProfileCreate(BaseModel):
    profile_name: str = Field(..., min_length=1, max_length=100, description="Profile full name or nickname")
    category: ProfileCategory = Field(default=ProfileCategory.OTHER, description="Profile category group")
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Birth latitude in decimal degrees")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Birth longitude in decimal degrees")
    location_name: Optional[str] = Field(default=None, description="Human readable geocoded place name")
    local_datetime: str = Field(..., description="Local birth datetime in ISO-8601 (YYYY-MM-DDTHH:MM:SS)")
    is_favorite: bool = Field(default=False, description="Flag indicating favorite bookmark")


class ProfileUpdate(BaseModel):
    profile_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    category: Optional[ProfileCategory] = None
    latitude: Optional[float] = Field(default=None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(default=None, ge=-180.0, le=180.0)
    location_name: Optional[str] = None
    local_datetime: Optional[str] = None
    is_favorite: Optional[bool] = None


class ProfileSummary(BaseModel):
    id: str
    profile_name: str
    category: str
    location_name: Optional[str] = None
    local_datetime: str
    iana_timezone: str
    sun_sign: Optional[str] = None
    moon_sign: Optional[str] = None
    ascendant_sign: Optional[str] = None
    is_favorite: bool
    created_at: str
    updated_at: str


class ProfileDetail(BaseModel):
    id: str
    profile_name: str
    category: str
    latitude: float
    longitude: float
    location_name: Optional[str] = None
    local_datetime: str
    iana_timezone: str
    utc_timestamp: str
    julian_day: float
    is_favorite: bool
    cached_western: Optional[Dict[str, Any]] = None
    cached_vedic: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str


class ProfileListResponse(BaseModel):
    status: str = "success"
    total_count: int
    profiles: List[ProfileSummary]


class ProfileSingleResponse(BaseModel):
    status: str = "success"
    profile: ProfileDetail

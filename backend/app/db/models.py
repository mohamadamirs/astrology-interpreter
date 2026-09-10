"""
SQLAlchemy Data Models for Chart Storage (FEAT-03)
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import (
    Column,
    String,
    Float,
    Boolean,
    DateTime,
    JSON
)
from backend.app.db.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class SavedChart(Base):
    __tablename__ = "saved_charts"

    id = Column(String(36), primary_key=True, default=generate_uuid, index=True)
    user_id = Column(String(36), nullable=True, index=True)
    profile_name = Column(String(100), nullable=False, index=True)
    category = Column(String(20), nullable=False, default="OTHER", index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    location_name = Column(String(255), nullable=True)
    local_datetime = Column(String(30), nullable=False)
    iana_timezone = Column(String(50), nullable=False)
    utc_timestamp = Column(String(30), nullable=False, index=True)
    julian_day = Column(Float, nullable=False)
    cached_western = Column(JSON, nullable=True)
    cached_vedic = Column(JSON, nullable=True)
    is_favorite = Column(Boolean, default=False, nullable=False, index=True)
    is_deleted = Column(Boolean, default=False, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), default=get_utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=get_utc_now, onupdate=get_utc_now, nullable=False)

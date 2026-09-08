# Skema Basis Data & Model Data

**Target:** PostgreSQL 16+ (Produksi) / SQLite 3 (Dev) | **ORM:** SQLAlchemy 2.0

---

## 1. Diagram Relasi Entitas (ERD)

```mermaid
erDiagram
    USERS ||--o{ SAVED_CHARTS : memiliki
    SAVED_CHARTS ||--o{ INTERPRETATION_LOGS : dievaluasi

    USERS {
        uuid id PK
        varchar email UK
        varchar hashed_password
        jsonb preferences
        timestamptz created_at
    }

    SAVED_CHARTS {
        uuid id PK
        uuid user_id FK
        varchar profile_name
        date birth_date
        time birth_time
        numeric latitude
        numeric longitude
        varchar iana_timezone
        numeric utc_offset_hours
        timestamptz normalized_utc
        varchar ayanamsha_system
        numeric ascendant_sidereal_deg
        numeric moon_sidereal_deg
        varchar birth_nakshatra
        int birth_pada
        jsonb computed_payload
        timestamptz created_at
    }

    HOURLY_TRANSIT_CACHE {
        timestamptz timestamp_hour_utc PK
        varchar ayanamsha_system PK
        jsonb planetary_positions
        jsonb aspect_matrix
        timestamptz cached_at
    }

    INTERPRETATION_LOGS {
        uuid id PK
        uuid chart_id FK
        timestamptz target_timestamp_utc
        int mental_score
        int emotional_score
        int career_score
        int interpersonal_score
        int vitality_score
        varchar verdict_summary
        jsonb raw_analysis_result
        timestamptz created_at
    }
```

---

## 2. Indeks Esensial

```sql
CREATE INDEX idx_saved_charts_user_id ON saved_charts(user_id);
CREATE INDEX idx_saved_charts_lat_lon ON saved_charts(latitude, longitude);
CREATE UNIQUE INDEX uq_user_chart_name ON saved_charts(user_id, profile_name);
CREATE INDEX idx_hourly_transit_lookup ON hourly_transit_cache(timestamp_hour_utc, ayanamsha_system);
CREATE INDEX idx_interpretation_timeline ON interpretation_logs(chart_id, target_timestamp_utc DESC);
```

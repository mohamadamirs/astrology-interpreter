# REST API Specification

**Base URL:** `/api/v1` | **Content-Type:** `application/json`

---

## 1. Global Envelopes

### 1.1 Success Envelope (HTTP 200)
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": { ... }
}
```

### 1.2 Error Envelope (HTTP 4xx / 5xx)
```json
{
  "success": false,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "error": {
    "code": "ERR_INVALID_COORDINATES",
    "message": "Latitude must be between -90.0 and 90.0 degrees.",
    "field": "latitude"
  }
}
```

---

## 2. Endpoints

### 2.1 `POST /geo/resolve-timezone`
Resolves coordinates to IANA timezone and UTC offset for a specific civil date.

* **Request:**
```json
{
  "latitude": -6.8700,
  "longitude": 109.0400,
  "civil_date": "2007-08-29",
  "civil_time": "06:40:00"
}
```
* **Response (200):**
```json
{
  "success": true,
  "data": {
    "iana_timezone": "Asia/Jakarta",
    "utc_offset_hours": 7.0,
    "is_dst_active": false,
    "calculated_utc_timestamp": "2007-08-28T23:40:00Z"
  }
}
```

### 2.2 `POST /chart/natal`
Calculates dual-zodiac planetary positions, Lagna, Nakshatras, and Vimshottari Dasha.

* **Request:**
```json
{
  "birth_date": "2007-08-29",
  "birth_time": "06:40:00",
  "latitude": -6.8700,
  "longitude": 109.0400,
  "ayanamsha": "lahiri",
  "house_system": "whole_sign"
}
```
* **Response (200 - Truncated):**
```json
{
  "success": true,
  "data": {
    "metadata": {
      "utc_birth_time": "2007-08-28T23:40:00Z",
      "resolved_timezone": "Asia/Jakarta",
      "ayanamsha_deg": 23.9641
    },
    "angles": {
      "ascendant_lagna": {
        "sidereal_deg": 145.5365,
        "formatted": "Leo 25°32'11\"",
        "nakshatra": "Purva Phalguni",
        "pada": 4,
        "sub_lord": "Mercury"
      }
    },
    "planets": {
      "sun": { "formatted": "Leo 11°13'05\"", "dignity": "Moolatrikona", "is_retrograde": false },
      "moon": { "formatted": "Aquarius 18°31'04\"", "nakshatra": "Shatabhisha", "pada": 4 }
    },
    "vimshottari_dasha": {
      "active_cycle": { "md": "Saturn", "ad": "Saturn", "pd": "Ketu", "sd": "Saturn" },
      "relationship_md_ad": "Self-Reinforcing"
    }
  }
}
```

### 2.3 `GET /transits/current`
Returns current celestial positions (Cached hourly).
* **Query:** `ayanamsha=lahiri`
* **Response (200):** Map of planets with sign, degree, speed, and retrograde status.

### 2.4 `POST /interpret/dynamic`
Evaluates transit-to-natal aspects and produces 5-domain scores.
* **Request:** `{"natal_chart_id": "UUID", "target_timestamp_utc": "ISO8601"}`
* **Response (200):**
  * `top_weighted_aspects`: List of active aspects with exact orb and weight.
  * `domain_barometer`: Integer scores & status for `mental_cognitive`, `emotional_psychological`, `career_situational`, `interpersonal_relational`, `physiological_vitality`.
  * `unvarnished_verdict`: Direct, non-flattering operational diagnosis.

---

## 3. Error Codes

| Code | Status | Cause |
| :--- | :---: | :--- |
| `ERR_INVALID_COORDINATES` | 422 | Lat $\notin [-90, 90]$ or Lon $\notin [-180, 180]$. |
| `ERR_DATE_OUT_OF_BOUNDS` | 400 | Date outside ephemeris range ($1800 - 2100\text{ CE}$). |
| `ERR_AYANAMSHA_UNSUPPORTED` | 400 | Invalid Ayanamsha key. |
| `ERR_CHART_NOT_FOUND` | 404 | Chart ID does not exist. |

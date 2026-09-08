# REST API Interface Specification

**Project Name:** Astrology-Interpreter API  
**Document ID:** API-ASTRO-001  
**Version:** 1.0.0  
**Status:** Approved for Implementation  
**Base URL:** `https://api.astrology-interpreter.internal/api/v1`  
**Protocol:** HTTPS | Content-Type: `application/json`  

---

## 1. Global Standards & Envelope Formats

### 1.1 Success Response Envelope
All successful HTTP 200 responses are encapsulated in a standard envelope:
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": { ... }
}
```

### 1.2 Error Response Envelope
All 4xx and 5xx client/server errors return a typed error envelope:
```json
{
  "success": false,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "error": {
    "code": "ERR_INVALID_COORDINATES",
    "message": "Latitude must be between -90.0 and 90.0 degrees.",
    "field": "latitude",
    "details": {
      "received_value": -95.21
    }
  }
}
```

### 1.3 Standard Error Code Catalog

| Error Code | HTTP Status | Root Cause & Description |
| :--- | :---: | :--- |
| `ERR_INVALID_COORDINATES` | 422 | Latitude $\notin [-90, 90]$ or Longitude $\notin [-180, 180]$. |
| `ERR_TIMEZONE_NOT_FOUND` | 404 | Coordinates fall in international waters with no resolved territorial zone. |
| `ERR_INVALID_DATE_FORMAT` | 422 | Date does not strictly adhere to ISO 8601 (`YYYY-MM-DD`). |
| `ERR_INVALID_TIME_FORMAT` | 422 | Time does not adhere to 24-hour format (`HH:MM:SS` or `HH:MM`). |
| `ERR_DATE_OUT_OF_BOUNDS` | 400 | Birth date falls outside high-precision ephemeris bounds ($1800 - 2100\text{ CE}$). |
| `ERR_AYANAMSHA_UNSUPPORTED` | 400 | Ayanamsha specified is not in `[lahiri, krishnamurti, raman, fagan_bradley]`. |
| `ERR_CHART_NOT_FOUND` | 404 | The requested persisted chart UUID does not exist. |

---

## 2. API Endpoints

### 2.1 Geospatial & Timezone Ingestion

#### `POST /geo/resolve-timezone`
Resolves physical geographic coordinates into an IANA timezone identifier and current civil offset.

* **Request Body:**
```json
{
  "latitude": -6.8700,
  "longitude": 109.0400,
  "civil_date": "2007-08-29",
  "civil_time": "06:40:00"
}
```

* **Response (HTTP 200):**
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": {
    "latitude": -6.8700,
    "longitude": 109.0400,
    "iana_timezone": "Asia/Jakarta",
    "utc_offset_hours": 7.0,
    "is_dst_active": false,
    "calculated_utc_timestamp": "2007-08-28T23:40:00Z"
  }
}
```

---

### 2.2 Natal Chart Calculation

#### `POST /chart/natal`
Performs complete Dual-Zodiac ephemeris positioning, house allocations, Nakshatra subdivisions, and Vimshottari Dasha sequence derivation.

* **Request Body:**
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

* **Response (HTTP 200):**
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": {
    "metadata": {
      "utc_birth_time": "2007-08-28T23:40:00Z",
      "resolved_timezone": "Asia/Jakarta",
      "ayanamsha_system": "lahiri",
      "ayanamsha_deg": 23.9641
    },
    "angles": {
      "ascendant_lagna": {
        "tropical_deg": 169.5006,
        "tropical_formatted": "Virgo 19°30'02\"",
        "sidereal_deg": 145.5365,
        "sidereal_formatted": "Leo 25°32'11\"",
        "nakshatra": "Purva Phalguni",
        "pada": 4,
        "nakshatra_lord": "Venus",
        "sub_lord": "Mercury",
        "navamsha_d9": "Scorpio"
      },
      "midheaven_mc": {
        "tropical_deg": 81.5954,
        "tropical_formatted": "Gemini 21°35'43\"",
        "sidereal_deg": 57.6313,
        "sidereal_formatted": "Taurus 27°37'52\"",
        "nakshatra": "Rohini",
        "pada": 4,
        "nakshatra_lord": "Moon",
        "sub_lord": "Ketu",
        "navamsha_d9": "Cancer"
      }
    },
    "planets": {
      "sun": {
        "tropical_deg": 155.1822,
        "sidereal_deg": 131.2181,
        "sign": "Leo",
        "sign_degree": 11.2181,
        "formatted": "Leo 11°13'05\"",
        "house": 1,
        "nakshatra": "Magha",
        "pada": 4,
        "nakshatra_lord": "Ketu",
        "sub_lord": "Saturn",
        "dignity": "Moolatrikona",
        "is_retrograde": false
      },
      "moon": {
        "tropical_deg": 342.4819,
        "sidereal_deg": 318.5178,
        "sign": "Aquarius",
        "sign_degree": 18.5178,
        "formatted": "Aquarius 18°31'04\"",
        "house": 7,
        "nakshatra": "Shatabhisha",
        "pada": 4,
        "nakshatra_lord": "Rahu",
        "sub_lord": "Moon",
        "dignity": "Neutral",
        "is_retrograde": false
      }
    },
    "vimshottari_dasha_baseline": {
      "birth_ruler": "Rahu",
      "balance_at_birth_years": 2.001,
      "target_active_dasha": {
        "mahadasha": "Saturn",
        "antardasha": "Saturn",
        "pratyantardasha": "Ketu",
        "sookshmadasha": "Saturn",
        "sookshma_remaining_days": 8.0,
        "relationship_md_ad": "Self-Reinforcing"
      }
    }
  }
}
```

---

### 2.3 Real-Time Transits

#### `GET /transits/current`
Returns instantaneous sky positions across Tropical and Sidereal frameworks for the current UTC moment.

* **Query Parameters:**
  * `ayanamsha` (optional, default: `lahiri`)

* **Response (HTTP 200):**
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": {
    "ayanamsha_deg": 24.2297,
    "positions": {
      "Sun": { "sidereal_sign": "Leo", "deg_in_sign": 21.028, "formatted": "Leo 21°01'41\"", "speed_deg_day": 0.974, "is_retrograde": false },
      "Moon": { "sidereal_sign": "Cancer", "deg_in_sign": 13.353, "formatted": "Cancer 13°21'12\"", "speed_deg_day": 12.145, "is_retrograde": false },
      "Saturn": { "sidereal_sign": "Pisces", "deg_in_sign": 18.630, "formatted": "Pisces 18°37'51\"", "speed_deg_day": -0.068, "is_retrograde": true }
    }
  }
}
```

---

### 2.4 Multi-Weighted Dynamic Interpretation

#### `POST /interpret/dynamic`
Executes mathematical transit-to-natal aspect mapping, exponential orb decay weighting, and 5-domain score aggregation.

* **Request Body:**
```json
{
  "natal_chart_id": "c7a8b69e-5e32-4bf1-a485-9b2f6b3e8c11",
  "target_timestamp_utc": "2026-09-08T07:25:00Z"
}
```

* **Response (HTTP 200):**
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": {
    "dasha_context": {
      "active_cycle": "Saturn-Saturn-Ketu-Saturn",
      "relationship": "Self-Reinforcing"
    },
    "top_weighted_aspects": [
      {
        "transit_body": "Uranus",
        "aspect": "Square",
        "natal_point": "sun",
        "orb_deg": 0.10,
        "weight": 13.04,
        "type": "Hard/Challenging",
        "hits_dasha_lord": false
      },
      {
        "transit_body": "Sun",
        "aspect": "Conjunction",
        "natal_point": "mercury",
        "orb_deg": 0.02,
        "weight": 9.72,
        "type": "Conjunction/Neutral",
        "hits_dasha_lord": false
      }
    ],
    "domain_barometer": {
      "mental_cognitive": {
        "score": 9,
        "status": "NEUTRAL / MIXED TENSION",
        "indicators": [
          "Transit Sun Conjunction Natal mercury (Orb 0.02°): High analytical capacity, rapid troubleshooting."
        ]
      },
      "emotional_psychological": {
        "score": -31,
        "status": "SEVERE FRICTION / HIGH VOLATILITY",
        "indicators": [
          "Transit Saturn Sesquiquadrate Natal saturn (Orb 0.26°): Vulnerability to boiling frustration, short fuse."
        ]
      },
      "career_situational": {
        "score": 25,
        "status": "CONSTRUCTIVE FLOW",
        "indicators": [
          "Transit Sun Conjunction Natal mercury: Tactical drive, courage to execute challenging tasks."
        ]
      },
      "interpersonal_relational": { "score": -8, "status": "MODERATE PRESSURE / IRRITATION", "indicators": [] },
      "physiological_vitality": { "score": -13, "status": "MODERATE PRESSURE / IRRITATION", "indicators": [] }
    },
    "unvarnished_verdict": {
      "core_dynamic": "Combustion of Will under Heavy Karmic Restriction",
      "strategic_imperative": "Do not burn relational or career bridges during peak friction. Direct the immense fire into isolated deep technical/intellectual work."
    }
  }
}
```

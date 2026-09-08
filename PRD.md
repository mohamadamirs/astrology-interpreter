# Product Requirements Document (PRD)

**Project Name:** Astrology-Interpreter Engine & Universal Platform  
**Document ID:** PRD-ASTRO-001  
**Version:** 1.0.0  
**Status:** Approved for Implementation  
**Target Release:** MVP (Phase 1)  

---

## 1. Document Overview & Objective

This document defines the strict functional, non-functional, mathematical, and architectural requirements for **Astrology-Interpreter**. The objective of the platform is to provide high-precision, mathematically deterministic astrological calculations and objective, anti-sycophantic psychological dynamic assessments across Mobile (iOS/Android) and Web environments.

---

## 2. Problem Statement & Value Proposition

### 2.1 Problem Statement
1. **Geospatial & Timezone Inaccuracies:** Traditional platforms rely on generic city centroids rather than physical coordinates, introducing errors of several arcminutes in the Ascendant (Lagna) and house cusps. Furthermore, historical Daylight Saving Time (DST) transitions are frequently mishandled.
2. **Interpretive Sycophancy & Cold-Reading Bias:** Consumer astrology products overwhelmingly deliver vague, universally flattering platitudes (the Forer/Barnum effect), failing to calculate structural frictions, malefic pressures, and objective behavioral liabilities.
3. **Platform Fragmentation:** Core calculation engines are typically decoupled from cross-platform client interfaces, preventing unified deployment across mobile and web targets.

### 2.2 Product Value Proposition
* **Sub-Arcsecond Precision:** Ephemeris-grade calculation based on raw geographic coordinates (GPS/Map picker) and offline astronomical algorithms.
* **Deterministic Multi-Weighted Decision Engine:** Mathematical mapping of Vimshottari Dasha cycles and transit aspects into quantifiable scores across 5 defined life domains with zero sugar-coating.
* **Universal Single-Codebase Architecture:** A high-performance Python (FastAPI) calculation backend powering a Universal React Native (Expo) client.

---

## 3. Scope of System

### 3.1 In-Scope (MVP Phase 1)
* Precise map-based geographic coordinate selection and automatic GPS detection.
* Fully offline coordinate-to-timezone resolution with historical DST accounting.
* Dual-Zodiac ephemeris engine (Sidereal Lahiri and Tropical Sayana).
* Complete Vedic divisions: 27 Nakshatras, 108 Padas, KP Sub-Lords, D1, and D9.
* Vimshottari Dasha engine resolving 4 hierarchical levels (MD, AD, PD, SD).
* Transit geometric aspect engine with exponential orb decay weighting.
* 5-Domain quantitative impact scoring engine (Mental, Emotional, Career, Interpersonal, Somatic).
* REST API exposing calculation, transit, and interpretation endpoints.
* Universal Expo client (Android, iOS, Web) with interactive map picker, chart renderer, and dashboard.

### 3.2 Out-of-Scope (Deferred to Post-MVP)
* Relational synastry / composite chart multi-user matching.
* Ashtakavarga numerical matrix calculation (Deferred to v1.2).
* Native payment gateway integration and subscription management.

---

## 4. Functional Requirements (FR)

### Module 1: Geospatial & Temporal Ingestion (GEO-TIME)

* **FR-GEO-01: Direct GPS Acquisition**
  * The system MUST provide a single-action trigger to capture device hardware GPS coordinates (WGS84) with latitude, longitude, and elevation.
* **FR-GEO-02: Interactive Map Coordinate Selection**
  * The system MUST provide an interactive map interface allowing the user to pan, zoom, and position a draggable pinpoint marker to any location globally.
  * The client MUST output coordinates rounded to 4 decimal places ($\pm 11$ meters precision).
* **FR-GEO-03: Offline IANA Timezone Resolution**
  * The backend MUST resolve arbitrary (Latitude, Longitude) tuples to an official IANA Timezone Identifier (e.g., `Asia/Jakarta`, `Europe/London`) strictly offline without reliance on third-party metered network APIs.
* **FR-GEO-04: Historical UTC Normalization**
  * Given a local civil date, civil time, and resolved IANA timezone, the backend MUST compute the exact historical UTC timestamp, correctly applying historical timezone offsets, war time, and daylight saving time (DST) valid on that specific date.

---

### Module 2: Ephemeris & Astronomical Positioning (ASTRO-CORE)

* **FR-AST-01: Planetary Coordinates**
  * The system MUST calculate the geocentric apparent ecliptic longitude, latitude, and daily velocity for: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.
* **FR-AST-02: Lunar Nodes (Rahu & Ketu)**
  * The system MUST calculate True and Mean Lunar Nodes. Ketu MUST remain exactly $180^\circ 00' 00"$ opposite to Rahu.
* **FR-AST-03: Retrogradation Detection**
  * The system MUST mark a celestial body as Retrograde (`is_retrograde = True`) if and only if its instantaneous daily longitudinal speed is negative ($\frac{d\lambda}{dt} < 0$), excluding Sun and Moon.
* **FR-AST-04: Dual Zodiac Transformation (Ayanamsha)**
  * The system MUST support Tropical (Sayana) and Sidereal (Nirayana) frameworks.
  * For Sidereal calculations, the engine MUST calculate IAU precession-based Ayanamsha for:
    1. Chitrapaksha / Lahiri (Default)
    2. Krishnamurti (KP)
    3. Raman
    4. Fagan-Bradley
* **FR-AST-05: House & Angle Derivations**
  * The system MUST calculate the Ascendant (Lagna) and Midheaven (MC) using exact Local Sidereal Time (RAMC) and geographic latitude.
  * The system MUST support Whole Sign, Placidus, and Equal house distribution systems.

---

### Module 3: Vedic Divisional Architecture (JYOTISH-CORE)

* **FR-JYO-01: Nakshatra and Pada Partitioning**
  * The engine MUST map any sidereal longitude $\lambda \in [0^\circ, 360^\circ)$ into one of 27 Nakshatras ($13^\circ 20'$ arc each) and one of 4 Padas ($3^\circ 20'$ arc each).
* **FR-JYO-02: KP Sub-Lord Proportional Arcs**
  * Each Nakshatra arc MUST be sub-divided into 9 unequal sub-divisions proportional to the Vimshottari period of each planet:
    $$\text{Arc Length (minutes)} = \frac{800 \times \text{Vimshottari Years}}{120}$$
* **FR-JYO-03: Divisional Charts (Vargas)**
  * The system MUST calculate D1 (Rashi) and D9 (Navamsha) divisional placements for all planets and the Lagna.
* **FR-JYO-04: Dignity Classifications**
  * The system MUST categorize each planet's condition into: Exalted (*Uchcha*), Moolatrikona, Own Sign (*Swakshetra*), Friendly (*Mitra*), Neutral (*Sama*), Enemy (*Shatru*), or Debilitated (*Neecha*).

---

### Module 4: Vimshottari Dasha Engine (DASHA-SYS)

* **FR-DSH-01: Natal Balance Computation**
  * The engine MUST compute the elapsed and remaining balance of the birth Nakshatra ruler from the exact sidereal longitude of the Moon at birth.
* **FR-DSH-02: 4-Tier Hierarchical Decomposition**
  * For any target timestamp $T \ge T_{\text{birth}}$, the engine MUST resolve:
    1. **Mahadasha (MD)** (Major period: 6 to 20 years)
    2. **Antardasha (AD)** (Sub-period: months to years)
    3. **Pratyantardasha (PD)** (Sub-sub-period: weeks to months)
    4. **Sookshmadasha (SD)** (Micro-period: days to weeks)
* **FR-DSH-03: Natural Relationship Matrix**
  * The engine MUST evaluate the baseline compatibility between the active MD ruler and AD ruler using classical *Nisargika Sambandha* (Great Friends, Friends, Neutral, Enemies, Bitter Mutual Enemies).

---

### Module 5: Transit Aspect & 5-Domain Interpretation Engine (INTERPRET-CORE)

* **FR-INT-01: Aspect Detection & Angular Distance**
  * The system MUST calculate minimum angular separation $\Delta\theta \in [0^\circ, 180^\circ]$ between transit bodies and natal points for:
    * Major Aspects: Conjunction ($0^\circ$), Sextile ($60^\circ$), Square ($90^\circ$), Trine ($120^\circ$), Opposition ($180^\circ$).
    * Minor Aspects: Semisquare ($45^\circ$), Sesquiquadrate ($135^\circ$), Quincunx ($150^\circ$).
* **FR-INT-02: Exponential Orb Weighting**
  * Aspect weights MUST be evaluated via continuous exponential decay:
    $$\text{Weight} = 10.0 \times e^{-1.4 \times \text{orb}}$$
  * If an aspect targets a planet currently active as the MD or AD ruler, its calculated weight MUST be amplified by $1.5\times$.
* **FR-INT-03: Quantitative 5-Domain Impact Mapping**
  * All transits and Dasha factors MUST map to integer score delta adjustments across 5 discrete domains:
    1. `mental_cognitive` (Cognitive load, analytical speed, overthinking)
    2. `emotional_psychological` (Emotional friction, tolerance threshold, composure)
    3. `career_situational` (Execution momentum, institutional friction, inertia)
    4. `interpersonal_relational` (Relational boundaries, friction, projection)
    5. `physiological_vitality` (Somatic tension, Pitta/Vata indicators, fatigue load)
* **FR-INT-04: Strict Anti-Sycophancy Constraints**
  * The system MUST NOT suppress negative scores or tone down malefic indicators.
  * Score labels MUST strictly follow:
    * $\le -40$: `SEVERE FRICTION / HIGH VOLATILITY`
    * $-39 \text{ to } -10$: `MODERATE PRESSURE / IRRITATION`
    * $-9 \text{ to } +9$: `NEUTRAL / MIXED TENSION`
    * $\ge +10$: `CONSTRUCTIVE FLOW`

---

### Module 6: Universal Client Interface (CLIENT-UI)

* **FR-UI-01: Cross-Platform Execution**
  * The user interface MUST compile and run identically across iOS, Android, and modern Web browsers (Chrome, Safari, Firefox) from a single shared React Native codebase.
* **FR-UI-02: Map Picker Modal**
  * The client MUST provide a full-screen or sheet modal hosting a map with live GPS centering and manual pin drop capabilities.
* **FR-UI-03: Chart Visualization Component**
  * The client MUST render crisp vector graphics (SVG) representing:
    * Vedic South Indian Chart format.
    * Vedic North Indian Diamond Chart format.
    * Western 360-Degree Circular Wheel.
* **FR-UI-04: Barometer & Verdict Display**
  * The client MUST render color-coded domain barometers reflecting the quantitative scores and output the unvarnished strategic verdict.

---

## 5. Non-Functional Requirements (NFR)

* **NFR-PERF-01 (Latency):** Backend computation of a full natal chart + Dasha hierarchy + current transit mapping MUST execute in $\le 150\text{ ms}$ on standard server hardware.
* **NFR-PERF-02 (Offline Lookup):** Offline timezone lookup via `timezonefinder` MUST complete in $\le 10\text{ ms}$ per coordinate request.
* **NFR-ACC-01 (Mathematical Accuracy):** Planetary longitude calculations MUST match Swiss Ephemeris benchmark data to within $\pm 0.001^\circ$ (3.6 arcseconds).
* **NFR-REL-01 (Determinism):** Identical input parameters (Date, Time, Lat, Lon, Ayanamsha) MUST produce bitwise-identical output JSON across all platforms.
* **NFR-SEC-01 (Privacy):** Coordinates ingested for natal calculations MUST NOT be transmitted to third-party ad networks or analytics services.

---

## 6. System Architecture & API Specification

### 6.1 Architecture Overview

```
[ Universal Client (Expo React Native) ]
   ├── MapView / Location Picker (expo-location + react-native-maps)
   ├── Chart Canvas (react-native-svg)
   └── State / Network Store (Axios / TanStack Query)
                   │
                   │ HTTPS JSON REST
                   ▼
[ Backend Engine (Python FastAPI) ]
   ├── /api/v1/geo/resolve-timezone (timezonefinder + zoneinfo)
   ├── /api/v1/chart/natal          (transit_engine: Natal calculations)
   ├── /api/v1/transits/current     (transit_engine: Real-time sky coordinates)
   └── /api/v1/interpret/dynamic    (interpreter_engine: Dasha & 5-Domain matrix)
```

### 6.2 Data Schemas & API Contracts

#### POST `/api/v1/chart/natal`
**Request Payload:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "NatalChartRequest",
  "type": "object",
  "required": ["birth_date", "birth_time", "latitude", "longitude"],
  "properties": {
    "birth_date": { "type": "string", "format": "date", "example": "2007-08-29" },
    "birth_time": { "type": "string", "pattern": "^[0-2][0-9]:[0-5][0-9](:[0-5][0-9])?$", "example": "06:40:00" },
    "latitude": { "type": "number", "minimum": -90.0, "maximum": 90.0, "example": -6.87 },
    "longitude": { "type": "number", "minimum": -180.0, "maximum": 180.0, "example": 109.04 },
    "ayanamsha": { "type": "string", "enum": ["lahiri", "krishnamurti", "raman", "fagan_bradley"], "default": "lahiri" }
  }
}
```

**Response Payload (Truncated Sample):**
```json
{
  "status": "success",
  "resolved_timezone": "Asia/Jakarta",
  "utc_timestamp": "2007-08-28T23:40:00Z",
  "ayanamsha": {
    "system": "lahiri",
    "value_deg": 23.9641
  },
  "ascendant": {
    "tropical_sign": "Virgo",
    "tropical_degree": 19.50,
    "sidereal_sign": "Leo",
    "sidereal_degree": 25.54,
    "nakshatra": "Purva Phalguni",
    "pada": 4,
    "sub_lord": "Mercury"
  },
  "planets": {
    "sun": {
      "tropical_degree": 155.42,
      "sidereal_degree": 131.22,
      "sign": "Leo",
      "degree_in_sign": 11.22,
      "nakshatra": "Magha",
      "pada": 4,
      "dignity": "Moolatrikona",
      "is_retrograde": false
    }
  }
}
```

---

## 7. Quality Gates & Acceptance Verification

| Requirement ID | Verification Method | Acceptance Benchmark |
| :--- | :--- | :--- |
| **FR-GEO-03** | Unit Test with 50 global coordinates | 100% correct IANA string match against benchmark database. |
| **FR-AST-04** | Regression comparison vs Swiss Ephemeris | Delta $\le 0.001^\circ$ for Sun, Moon, and 8 planets. |
| **FR-DSH-02** | Dasha timeline test vector | Exact MD, AD, PD date match against established astronomical tables. |
| **FR-INT-04** | Stress test with harsh malefic transit vector | Output MUST reflect negative domain score; zero flattery text emitted. |
| **FR-UI-01** | Multi-target build test | Codebase successfully packages into Android APK, iOS bundle, and Web SPA. |

---
*End of Specification.*

# Sequence Diagram 02: Time-Traveling Transit Engine & Aspect Hit Scanner

**Document ID:** SD-ASTRO-002  
**Related Features:** Feature 5 (Time-Traveling Transit Engine: Slider, Calendar, Aspect Hit Scanner)  
**Status:** Approved  

---

## 1. Scenario Description

This sequence diagram details two fundamental operations of the transit system:
1. **Time-Traveling Navigation (Slider & Calendar):** The user navigates backward or forward in time. The system queries the *Hourly Discrete Transit Cache* (ADR-0006) to retrieve planetary positions instantaneously with minimal CPU overhead, subsequently evaluating aspects against the user natal chart via exponential decay weighting (ADR-0005).
2. **Key Moment Finder (*Aspect Hit Scanner*):** The user selects a specific transit event (e.g., *"Transit Saturn Opposition Natal Sun"*). The system invokes a numerical root-finding solver (bisection / Newton-Raphson) to locate the exact date and second where the angular separation hits peak culmination ($0.000^\circ$ orb), smoothly updating the UI timeline directly to that milestone.

---

## 2. System Participants

* **User:** End user exploring transit timelines or seeking specific astrological milestones.
* **UI_App (Expo React Native):** `TransitController` component (Scrubber Slider, Heatmap Calendar, Scanner form).
* **API_Gateway (FastAPI):** Endpoints `/api/v1/transit/timeline` and `/api/v1/transit/scan-hit`.
* **TransitCacheService:** In-memory / Redis or database store managing discrete hourly planetary coordinates.
* **EphemerisCore:** High-precision `pyswisseph` astronomical solver computing geocentric positions and speeds.
* **AspectScoringEngine:** Exponential decay weighting algorithm $W(\delta) = 10.0 	imes \exp(-1.4 	imes \delta)$.
* **NumericalRootSolver:** Interpolative bisection algorithm locating minimum orb culmination points.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as UI_App (Transit View)
    participant API as API_Gateway (FastAPI)
    participant Cache as TransitCacheService (In-Memory/Redis)
    participant Ephem as EphemerisCore
    participant Score as AspectScoringEngine
    participant Solver as NumericalRootSolver

    %% Scenario A: Transit Timeline Navigation (Slider / Calendar)
    User->>UI: Scrub Time Slider to Target Date (e.g. 2026-11-15 14:00 UTC)
    UI->>API: GET /api/v1/transit/timeline?chart_id=uuid-1234&target_utc=2026-11-15T14:00:00Z
    activate API

    API->>Cache: get_discrete_ephemeris(2026-11-15, hour=14)
    activate Cache
    alt Cache Hit (Hourly Data Cached)
        Cache-->>API: cached_planetary_positions[]
    else Cache Miss (Not Yet Computed)
        Cache-->>API: null
        API->>Ephem: compute_planetary_positions(target_julian_day)
        Ephem-->>API: calculated_positions[]
        API->>Cache: store_discrete_ephemeris(2026-11-15, hour=14, calculated_positions)
    end
    deactivate Cache

    API->>Score: calculate_transit_to_natal_aspects(natal_chart, transit_positions)
    activate Score
    Note over Score: Calculate angular separation $\delta$ for all planet pairs<br/>Apply formula: $W(\delta) = 10 	imes \exp(-1.4 	imes \delta)$<br/>Identify active aspects (orb <= 6 degrees)
    Score-->>API: active_aspects_list[] with exact_orbs and weights
    deactivate Score

    API-->>UI: HTTP 200 OK: {transit_positions, active_aspects, dominant_themes}
    deactivate API

    UI->>UI: Animate Celestial Bodies on Wheel & List Active Aspects
    UI-->>User: Display Sky Positions & Impact Summary for Selected Day

    %% Scenario B: Aspect Hit Scanner (Key Moment Finder)
    User->>UI: Select "Hit Scanner" (Target: "Saturn Opposition Sun", Span: 2026-2027)
    UI->>API: POST /api/v1/transit/scan-hit {natal_planet: "Sun", transit_planet: "Saturn", aspect_type: "opposition", start_year: 2026, end_year: 2027}
    activate API

    API->>Solver: scan_exact_aspect_hits("Saturn", "Sun", 180.0, 2026_01_01, 2027_12_31)
    activate Solver
    Note over Solver: 1. Coarse Scan: Sample coordinates every 5 days<br/>2. Detect angular difference zero-crossings<br/>3. Fine Scan: Bisection / Newton-Raphson until orb < 0.001 deg
    Solver->>Ephem: compute_positions_at_epoch(interpolated_jd)
    Ephem-->>Solver: precise_positions
    Solver-->>API: list_of_exact_hits [ {exact_utc: "2026-08-14T03:22:15Z", peak_orb: 0.0001, is_retrograde: true} ]
    deactivate Solver

    API-->>UI: HTTP 200 OK: {hits: [...], message: "Found 1 exact hit"}
    deactivate API

    UI-->>User: Display List of Exact Culmination Hit Dates
    User->>UI: Click Exact Hit Result
    UI->>UI: Jump Timeline Scrubber to Selected Hit Date
    UI-->>User: Render Exact Sky Configuration at Culmination Moment
```

---

## 4. Edge Case Handling

| Edge Case | Risk | Mitigation Mechanism |
| :--- | :--- | :--- |
| **Triple Hit via Retrograde Loops** | Outer planets (Saturn/Jupiter) transit an exact point three times (direct $ightarrow$ retrograde $ightarrow$ direct). | The solver detects daily motion velocity sign flips and aggregates the three hits into a cohesive *"Tri-Hit Transit Cycle"*. |
| **Excessively Wide Scan Window (>50 years)** | Backend request timeout from long calculation loops. | Impose a maximum scan window of 5 years per single API call, returning continuation tokens for subsequent pagination. |
| **Circular Coordinate Discontinuity ($360^\circ \leftrightarrow 0^\circ$)** | Angle differences jumping from $359.9^\circ$ to $0.1^\circ$ (modular wrap-around). | Use minimal circular difference calculation: $\Delta	heta = \min(|	heta_1 - 	heta_2|, 360^\circ - |	heta_1 - 	heta_2|)$. |

---

## 5. Contract Data Structure

### Request: `POST /api/v1/transit/scan-hit`
```json
{
  "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "transit_body": "Saturn",
  "natal_body": "Sun",
  "aspect_angle": 180.0,
  "date_range": {
    "start_utc": "2026-01-01T00:00:00Z",
    "end_utc": "2027-12-31T23:59:59Z"
  }
}
```

### Response: `HTTP 200 OK`
```json
{
  "status": "success",
  "total_hits_found": 1,
  "hits": [
    {
      "hit_number": 1,
      "exact_utc": "2026-08-14T03:22:15Z",
      "transit_body_longitude": 335.1204,
      "natal_body_longitude": 155.1200,
      "exact_aspect_angle": 180.0004,
      "orb": 0.0004,
      "is_retrograde": true,
      "weight_score": 10.0,
      "affected_domains": ["Career/Situational", "Mental/Cognitive"]
    }
  ]
}
```

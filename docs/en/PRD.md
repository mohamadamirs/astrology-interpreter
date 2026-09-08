# Product Requirements Document (PRD)

## 1. Product Vision
A high-precision, cross-platform astrology engine (Mobile & Web) eliminating two industry flaws:
1. **Centroid Coordinate Inaccuracy:** Replaces generic city lookups with physical GPS acquisition and map pin-drop coordinates.
2. **Interpretive Sycophancy (Barnum Effect):** Replaces vague flattery with a deterministic 5-domain scoring engine that maps friction and constructive flow objectively.

---

## 2. System Scope

### 2.1 In-Scope (MVP)
* Map pin-drop coordinate selection ($\pm 11\text{m}$ precision) and automatic device GPS ingestion.
* Offline IANA timezone resolution and historical UTC offset normalization (including DST).
* Dual-Zodiac calculations: Tropical (Sayana) and Sidereal (Lahiri default, KP, Raman, Fagan-Bradley).
* Vedic subdivisions: 27 Nakshatras, 108 Padas, KP Sub-Lords, D1 (Rashi), D9 (Navamsha).
* 4-tier hierarchical Vimshottari Dasha engine (MD, AD, PD, SD).
* Transit geometric aspect engine with continuous exponential orb decay weighting ($W = 10 \cdot e^{-1.4 \cdot \text{orb}}$).
* 5-Domain impact scoring: Mental, Emotional, Career, Interpersonal, Vitality.
* Universal client (iOS, Android, Web via Expo) rendering interactive SVG charts (Vedic South/North & Western wheel).

### 2.2 Out-of-Scope (Post-MVP)
* Multi-user synastry / composite charts.
* Full Ashtakavarga numerical matrix computation.
* Native payment gateway and subscription workflows.

---

## 3. Functional Requirements

### 3.1 Geospatial & Time Ingestion (`GEO-TIME`)
* **FR-GEO-01:** Client must capture hardware GPS coordinates via `expo-location`.
* **FR-GEO-02:** Client must provide an interactive map with draggable pin outputting WGS84 latitude/longitude to 4 decimal places.
* **FR-GEO-03:** Backend must resolve coordinates to an official IANA timezone (e.g., `Asia/Jakarta`) 100% offline via polygon lookup (`timezonefinder`).
* **FR-GEO-04:** Backend must compute canonical UTC timestamp using Python `zoneinfo`, accounting for historical DST valid on the birth date.

### 3.2 Ephemeris & Astronomical Positioning (`ASTRO-CORE`)
* **FR-AST-01:** Compute geocentric apparent ecliptic longitude, latitude, and daily velocity for Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto.
* **FR-AST-02:** Compute True and Mean Lunar Nodes (Ketu must remain exactly $180^\circ$ opposite to Rahu).
* **FR-AST-03:** Flag retrograde status (`is_retrograde = True`) if and only if daily longitudinal velocity $< 0$ (excluding Sun and Moon).
* **FR-AST-04:** Derive RAMC, Ascendant (Lagna), and Midheaven (MC) from Local Sidereal Time. Support Whole Sign, Placidus, and Equal house systems.
* **FR-AST-05:** Convert tropical positions to sidereal via IAU precession-based Ayanamsha subtraction: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropical}} - \text{Ayanamsha}) \pmod{360^\circ}$.

### 3.3 Vedic Divisions & Dasha Engine (`JYOTISH-CORE`)
* **FR-JYO-01:** Partition sidereal longitudes into 27 Nakshatras ($13^\circ 20'$ each) and 4 Padas ($3^\circ 20'$ each).
* **FR-JYO-02:** Derive KP Sub-Lord using proportional Vimshottari arcs: $\text{Arc} = (800' \times \text{Years}) / 120$.
* **FR-JYO-03:** Compute D1 (Rashi) and D9 (Navamsha) sign placements and planetary dignities (Exalted, Moolatrikona, Own Sign, Neutral, Debilitated).
* **FR-JYO-04:** Calculate Vimshottari Dasha 4-tier hierarchy (MD, AD, PD, SD) and natural relationship matrix (*Nisargika Sambandha*) between active MD and AD rulers.

### 3.4 Transit Engine & 5-Domain Scoring (`INTERPRET-CORE`)
* **FR-INT-01:** Detect angular separation for Conjunction ($0^\circ$), Sextile ($60^\circ$), Square ($90^\circ$), Trine ($120^\circ$), Opposition ($180^\circ$), Semisquare ($45^\circ$), Sesquiquadrate ($135^\circ$), Quincunx ($150^\circ$).
* **FR-INT-02:** Calculate aspect weight via exponential decay: $W = 10.0 \times e^{-1.4 \times \text{orb}}$. Apply $1.5\times$ multiplier if aspect targets active MD or AD ruler.
* **FR-INT-03:** Map transit aspects and Dasha baseline into integer score deltas across 5 domains:
  * `mental_cognitive` (Focus, analytical capacity vs overthinking)
  * `emotional_psychological` (Composure vs friction/frustration)
  * `career_situational` (Execution drive vs structural friction)
  * `interpersonal_relational` (Relational boundaries vs projection)
  * `physiological_vitality` (Somatic tension, Pitta/Vata indicators)
* **FR-INT-04:** Strictly enforce score categories:
  * $\le -40$: `SEVERE FRICTION / HIGH VOLATILITY`
  * $-39 \text{ to } -10$: `MODERATE PRESSURE / IRRITATION`
  * $-9 \text{ to } +9$: `NEUTRAL / MIXED TENSION`
  * $\ge +10$: `CONSTRUCTIVE FLOW`

### 3.5 Universal Client Interface (`CLIENT-UI`)
* **FR-UI-01:** Single React Native codebase targeting iOS, Android, and Web browsers.
* **FR-UI-02:** Render crisp vector charts (SVG) for Vedic South Indian, Vedic North Indian, and Western 360° Circular Wheel formats.
* **FR-UI-03:** Render color-coded 5-domain barometer cards and unvarnished strategic verdict.

---

## 4. Non-Functional Requirements (NFR)
* **NFR-PERF-01 (Latency):** Full natal calculation + Dasha + current transit mapping $\le 150\text{ ms}$.
* **NFR-PERF-02 (Offline Lookup):** Coordinate-to-timezone resolution $\le 10\text{ ms}$ with zero network queries.
* **NFR-ACC-01 (Precision):** Planetary longitudes match Swiss Ephemeris / NASA JPL benchmark vectors within $\pm 0.001^\circ$ ($3.6$ arcseconds).
* **NFR-DET-01 (Determinism):** Identical inputs must yield bitwise-identical JSON responses.
* **NFR-PRIV-01 (Privacy):** Geographic coordinates must not be transmitted to external telemetry or third-party ad services.

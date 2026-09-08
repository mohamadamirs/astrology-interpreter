# Technical Architecture & System Design

## 1. System Topology

A decoupled, stateless compute architecture:
* **Backend:** Python (FastAPI) handling astronomical mathematics, offline spatial timezone lookups, and deterministic scoring.
* **Frontend:** Universal React Native (Expo) targeting Android, iOS, and Web (SPA) via `react-native-web`.
* **Database:** PostgreSQL (Production) / SQLite (Development) with SQLAlchemy 2.0 ORM.

```
[ Expo Client (iOS / Android / Web) ]
   ├── LocationPicker (expo-location + react-native-maps)
   ├── ChartCanvas (react-native-svg)
   └── Store (Zustand + TanStack Query)
                 │  HTTPS JSON REST
                 ▼
[ FastAPI Backend (Python) ]
   ├── GeoTimeService (timezonefinder + zoneinfo)
   ├── EphemerisService (pyephem / pyswisseph)
   ├── JyotishEngine (Nakshatra, Pada, KP Sub-Lord, Dignity)
   ├── DashaEngine (Vimshottari 4-tier traversal)
   ├── TransitEngine (Aspects + Exponential Decay)
   └── ScoringEngine (5-Domain Accumulator)
                 │
                 ▼
[ PostgreSQL / SQLite ]
```

---

## 2. Directory Structure

```text
backend/
├── app/
│   ├── api/v1/endpoints/     # geo.py, chart.py, transits.py, interpret.py
│   ├── core/                 # config.py, constants.py, exceptions.py
│   ├── engine/               # PURE ASTRONOMICAL LOGIC (Zero web dependencies)
│   │   ├── ephemeris.py      # Lon/lat/speed & retrograde logic
│   │   ├── ayanamsha.py      # Lahiri, KP, Raman, Fagan-Bradley
│   │   ├── angles.py         # RAMC, Ascendant, Midheaven, House Cusps
│   │   ├── jyotish.py        # Nakshatras, Padas, KP Sub-Lords, Dignity
│   │   ├── dasha.py          # Vimshottari MD/AD/PD/SD calculations
│   │   ├── aspects.py        # Angular separation & exponential weighting
│   │   └── scoring.py        # 5-Domain quantitative scoring matrix
│   ├── models/               # SQLAlchemy models (User, SavedChart, TransitCache)
│   ├── schemas/              # Pydantic request/response validation schemas
│   └── services/             # Orchestration services
└── tests/                    # Pytest suite + ground truth benchmark vectors

frontend/
├── src/
│   ├── api/                  # Axios clients & TanStack Query hooks
│   ├── components/           # Button, Card, Modal, Typography
│   ├── features/
│   │   ├── location-picker/  # GPS button & interactive map picker
│   │   ├── chart-viewer/     # SVG Vedic South/North & Western wheel
│   │   ├── domain-barometer/ # Gauge cards & unvarnished verdict display
│   │   └── natal-form/       # Date/time inputs & Zodiac toggle
│   └── store/                # Zustand client state
└── app/                      # Expo Router screens
```

---

## 3. Core Mathematical Pipelines

### 3.1 Geospatial & Historical UTC Pipeline
1. Ingest $(Lat, Lon)$ $\rightarrow$ Query `timezonefinder` offline $\rightarrow$ Get IANA string (e.g. `Asia/Jakarta`).
2. Resolve local civil datetime via `zoneinfo.ZoneInfo(tz_name)` $\rightarrow$ Automatically calculate historical DST offset $\rightarrow$ Derive canonical UTC timestamp.

### 3.2 Ascendant & Ecliptic Projection Pipeline
1. Compute Greenwich Sidereal Time ($GST$) from Julian Date $JD$.
2. Compute Local Sidereal Time: $\theta_L = (GST + \text{lon}) \pmod{360^\circ}$.
3. Calculate Ascendant:
   $$\tan(\text{Asc}) = \frac{\cos(\theta_L)}{-\sin(\theta_L)\cos(\epsilon) - \tan(\phi)\sin(\epsilon)}$$
4. Compute Sidereal Longitude: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropical}} - \text{Ayanamsha}) \pmod{360^\circ}$.

### 3.3 Vimshottari Traversal Pipeline
1. Extract Moon's Sidereal Longitude ($\lambda_{\text{Moon}}$) and find Nakshatra index.
2. Determine fraction passed and balance of birth Nakshatra ruler.
3. Advance through cycle array `[Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17)]` to isolate exact MD, AD, PD, and SD at target date.

### 3.4 Continuous Aspect Weighting Pipeline
For transit aspect with angular error $\delta$ (orb in degrees):
$$W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$$
Apply scalar $W_{\text{effective}} = W(\delta) \times 1.5$ if aspect touches active MD or AD ruler.

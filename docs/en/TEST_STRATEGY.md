# Quality Assurance & Test Strategy

## 1. Core Principles
* **Mathematical Determinism:** Identical inputs must yield bitwise-identical output.
* **Ephemeris Benchmark Tolerance:** Planetary positions must match Swiss Ephemeris / JPL benchmark vectors within $\pm 0.001^\circ$ (3.6 arcseconds).
* **Zero Runtime Network I/O in Tests:** Timezone lookups must run purely against local polygon data.

---

## 2. Ground Truth Benchmark Vectors

### Vector 1: Standard Equatorial / Low-Latitude Reference
* **Input:** `2007-08-29 06:40:00 WIB` (`2007-08-28 23:40:00 UTC`), Lat `-6.8700`, Lon `109.0400` (Brebes).
* **Expected Ground Truth:**
  * Ascendant (Lagna): Sidereal Leo $25^\circ 32' \pm 0.05^\circ$ (*Purva Phalguni 4*).
  * Moon (Chandra): Sidereal Aquarius $18^\circ 31' \pm 0.02^\circ$ (*Shatabhisha 4*).
  * Sun (Surya): Sidereal Leo $11^\circ 13' \pm 0.01^\circ$ (*Magha 4*).
  * Dasha at 2026-09-08: Mahadasha **Saturn**, Antardasha **Saturn** (*Swabhukti*).

### Vector 2: Exact Conjunction (Total Solar Eclipse)
* **Input:** `1999-08-11 11:03:00 UTC`, Lat `48.1351`, Lon `11.5820` (Munich).
* **Expected Ground Truth:**
  * Sun and Moon Tropical longitudes match within $\Delta \le 0.001^\circ$.
  * Aspect engine reports Conjunction with orb $\le 0.002^\circ$.

### Vector 3: Polar Latitude Cusps (Placidus Fallback)
* **Input:** `2024-12-21 12:00:00 UTC`, Lat `69.6492`, Lon `18.9553` (Tromsø, Norway).
* **Expected Ground Truth:**
  * System detects polar circle quadrant breakdown and cleanly falls back to Whole Sign without division-by-zero.

---

## 3. Test Matrix & Frameworks

| Layer | Tools | Target Metrics |
| :--- | :--- | :--- |
| **Engine Units** | `pytest`, `pytest-cov` | Coverage $\ge 90\%$; benchmark delta $\le 0.001^\circ$. |
| **API Integration** | `httpx.AsyncClient` | 100% schema validation, status codes, error payloads. |
| **Client UI** | `jest`, React Native Testing Library | Map event triggers, chart SVG mounting. |

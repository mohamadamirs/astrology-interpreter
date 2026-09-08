# Quality Assurance & Verification Strategy

**Project Name:** Astrology-Interpreter  
**Document ID:** QA-ASTRO-001  
**Version:** 1.0.0  
**Status:** Approved for Implementation  
**Companion Documents:** [PRD.md](./PRD.md) | [ARCHITECTURE.md](./ARCHITECTURE.md)  

---

## 1. Testing Philosophy & Quality Standard

Because this platform is designed as a **mathematically deterministic system**, testing is not merely concerned with UI responsiveness, but strictly with **astronomical accuracy, floating-point stability, and boundary determinism**. 

* **Rule 1:** Ephemeris positioning must match Swiss Ephemeris / JPL Horizons ground truth benchmarks within $\pm 0.001^\circ$ ($3.6$ arcseconds).
* **Rule 2:** Timezone normalization must never rely on runtime network queries during test runs.
* **Rule 3:** The interpretation scoring engine must be 100% deterministic: given constant inputs, domain scores must yield bitwise-identical values.

---

## 2. Testing Levels & Tooling Suite

| Level | Target | Framework | Success Criteria |
| :--- | :--- | :--- | :--- |
| **Unit Testing (Backend)** | Math & Core Logic | `pytest`, `pytest-cov` | Line coverage $\ge 90\%$, Branch coverage $\ge 85\%$. |
| **Benchmark Regression** | Ephemeris & Ayanamsha | Custom Vector Harness | Maximum error $\le 0.001^\circ$ across all celestial bodies. |
| **Integration Testing** | FastAPI Endpoints | `httpx.AsyncClient` | 100% contract adherence, strict JSON schema validation. |
| **Client Unit & E2E** | React Native (Expo) | `jest`, `@testing-library/react-native` | Component mounting, map picker event emission, SVG render. |

---

## 3. Mandatory Astronomical Ground Truth Test Vectors

Every automated CI pipeline execution must run against a fixed suite of historical ground truth test vectors:

### Vector 1: Standard Equatorial / Low-Latitude Reference
* **Date & Time:** `2007-08-29 06:40:00 WIB` (`2007-08-28 23:40:00 UTC`)
* **Coordinates:** `Lat -6.8700, Lon 109.0400` (Brebes, Indonesia)
* **Ayanamsha:** Lahiri ($23^\circ 57' 50" \pm 2"$)
* **Expected Ground Truth Assertions:**
  * Ascendant (Lagna): Sidereal Leo $25^\circ 32' \pm 0.05^\circ$ (*Purva Phalguni Pada 4*).
  * Moon (Chandra): Sidereal Aquarius $18^\circ 31' \pm 0.02^\circ$ (*Shatabhisha Pada 4*).
  * Sun (Surya): Sidereal Leo $11^\circ 13' \pm 0.01^\circ$ (*Magha Pada 4*).
  * Active Dasha at 2026-09-08: Mahadasha = **Saturn**, Antardasha = **Saturn** (*Swabhukti*).

### Vector 2: Exact Celestial Alignment (Total Solar Eclipse)
* **Date & Time:** `1999-08-11 11:03:00 UTC`
* **Coordinates:** `Lat 48.1351, Lon 11.5820` (Munich, Germany)
* **Expected Ground Truth Assertions:**
  * Sun and Moon Tropical Longitudes MUST match within $\Delta \le 0.001^\circ$ (Exact Conjunction).
  * Aspect engine must report Conjunction with orb $\le 0.002^\circ$.

### Vector 3: Extreme Latitude Polar House Cusps
* **Date & Time:** `2024-12-21 12:00:00 UTC` (Winter Solstice / Polar Night)
* **Coordinates:** `Lat 69.6492, Lon 18.9553` (Tromsø, Norway)
* **Expected Ground Truth Assertions:**
  * Placidus house quadrant division algorithm MUST either compute gracefully without division-by-zero or cleanly fallback to Whole Sign / Equal house system.

### Vector 4: Planet Stationary / Retrograde Transition
* **Target:** Saturn stationing retrograde.
* **Expected Ground Truth Assertions:**
  * Instantaneous speed transition from $+0.001^\circ/\text{day}$ to $-0.001^\circ/\text{day}$ correctly switches `is_retrograde` boolean flag without NaN errors.

---

## 4. Edge Case & Failure Mode Matrix

| Scenario | Simulated Input | Expected System Behavior |
| :--- | :--- | :--- |
| **DST "Spring Forward" Void** | `2024-03-31 02:30:00` in London (clock jumped from 01:59 to 03:00). | Backend resolves to legal non-existent time fallback (03:30:00 BST) with notice. |
| **DST "Fall Back" Ambiguity** | `2024-10-27 01:30:00` in London (hour repeated twice). | System defaults to standard time offset with warning flag. |
| **Equator & Prime Meridian** | `Lat 0.0000, Lon 0.0000` (Gulf of Guinea). | System resolves coordinates without sign-flip errors; assigns GMT. |
| **Date Boundary Overflow** | `2024-12-31 23:59:59` at `UTC+14` (Kiribati). | Correctly maps to `2024-12-31 09:59:59 UTC` without rolling year forward prematurely. |

---

## 5. Continuous Integration (CI) Quality Gates

The GitHub Actions workflow enforces the following gates before any pull request may merge:

```yaml
# Conceptual CI Pipeline Gate:
- name: Run Backend Unit & Benchmark Tests
  run: |
    pytest --cov=app --cov-report=term-missing --cov-fail-under=90
    python scripts/verify_ephemeris_benchmarks.py --max-delta=0.001

- name: Linting & Static Typing
  run: |
    ruff check app/
    mypy app/ --strict

- name: Universal Frontend Tests
  run: |
    cd frontend && npm test -- --coverage --watchAll=false
```

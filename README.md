# Astrology-Interpreter Platform

High-precision, mathematically deterministic astrological calculation engine and zero-sycophancy psychological dynamics interpretation platform.

---

## 📚 Complete Pre-Development Documentation Suite

Before beginning codebase implementation, review the comprehensive architectural and engineering specifications in the [`docs/`](./docs) directory:

| Document | Identifier | Focus & Purpose |
| :--- | :--- | :--- |
| **[PRD (Product Requirements)](./docs/PRD.md)** | `PRD-ASTRO-001` | Functional scope, anti-sycophancy rules, and user capabilities. |
| **[System Architecture & TDD](./docs/ARCHITECTURE.md)** | `ARCH-ASTRO-001` | Technical design, clean architecture patterns, algorithmic pipelines. |
| **[API Specification & Contracts](./docs/API_SPEC.md)** | `API-ASTRO-001` | REST endpoints, JSON payload schemas, and typed error catalog. |
| **[Database Schema & Models](./docs/DATA_SCHEMA.md)** | `DATA-ASTRO-001` | Entity-Relationship Diagram (ERD), PostgreSQL/SQLite tables & indexes. |
| **[QA & Verification Strategy](./docs/TEST_STRATEGY.md)** | `QA-ASTRO-001` | Ground truth test vectors, ephemeris tolerances, and CI quality gates. |
| **[Roadmap & Developer Backlog](./docs/ROADMAP_AND_BACKLOG.md)** | `RDM-ASTRO-001` | Sprint breakdown, granular task list, and Definition of Done (DoD). |
| **[Architecture Decision Records (ADRs)](./docs/adr/README.md)** | `ADR-0001..0006` | Recorded technical decisions, rationale, trade-offs, and rejected options. |

---

## 🏛️ Technology Stack

* **Backend Compute Engine:** Python 3.11+ | [FastAPI](https://fastapi.tiangolo.com/) | [PyEphem](https://rhodesmill.org/pyephem/) | [TimeZoneFinder](https://github.com/mrJean1/timezonefinder)
* **Presentation Tier:** Universal [React Native](https://reactnative.dev/) | [Expo](https://expo.dev/) (Android, iOS, Web via `react-native-web`)
* **Persistence & Migrations:** PostgreSQL 16+ / SQLite 3 | SQLAlchemy 2.0 | Alembic
* **Quality Assurance:** Pytest | Ruff | Mypy (Strict) | Jest | Swiss Ephemeris Test Harness

---

## ⚡ Core Principles

1. **Deterministic Mathematics:** Zero approximations. All ephemeris and divisional placements are computed to sub-arcsecond tolerances from raw geographic coordinates.
2. **Zero Sycophancy:** The interpretation scoring engine strictly evaluates natural planetary enmities and malefic aspects without sugar-coating or cold-reading rationalizations.
3. **Universal Single Codebase:** Shared business logic and cross-platform UI targeting mobile and desktop browsers simultaneously.

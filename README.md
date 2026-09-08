# Astrology-Interpreter Platform

High-precision, mathematically deterministic astrological calculation engine and zero-sycophancy psychological dynamics interpretation platform.

---

## 📚 Documentation / Dokumentasi

Choose your language / Pilih bahasa Anda:

| Language | Entry Point | Core Files |
| :--- | :--- | :--- |
| 🇬🇧 **English** | **[docs/en/README.md](./docs/en/README.md)** | [PRD](./docs/en/PRD.md) • [Architecture](./docs/en/ARCHITECTURE.md) • [API](./docs/en/API_SPEC.md) • [Schema](./docs/en/DATA_SCHEMA.md) • [QA](./docs/en/TEST_STRATEGY.md) • [Roadmap](./docs/en/ROADMAP.md) • [ADRs](./docs/en/adr/README.md) |
| 🇮🇩 **Bahasa Indonesia** | **[docs/id/README.md](./docs/id/README.md)** | [PRD](./docs/id/PRD.md) • [Arsitektur](./docs/id/ARCHITECTURE.md) • [API](./docs/id/API_SPEC.md) • [Skema Data](./docs/id/DATA_SCHEMA.md) • [QA](./docs/id/TEST_STRATEGY.md) • [Roadmap](./docs/id/ROADMAP.md) • [ADR](./docs/id/adr/README.md) |

---

## 🏛️ Technology Stack

* **Backend Compute Engine:** Python 3.11+ | [FastAPI](https://fastapi.tiangolo.com/) | [PyEphem](https://rhodesmill.org/pyephem/) | [TimeZoneFinder](https://github.com/mrJean1/timezonefinder)
* **Presentation Tier:** Universal [React Native](https://reactnative.dev/) | [Expo](https://expo.dev/) (Android, iOS, Web via `react-native-web`)
* **Persistence & Migrations:** PostgreSQL 16+ / SQLite 3 | SQLAlchemy 2.0 | Alembic
* **Quality Assurance:** Pytest | Ruff | Mypy (Strict) | Jest | Swiss Ephemeris Benchmark Harness

---

## ⚡ Core Principles / Prinsip Utama

1. **Deterministic Mathematics / Matematika Deterministik:**  
   Sub-arcsecond celestial mechanics computed from raw GPS/map coordinates, with zero rounding shortcuts.
2. **Zero Sycophancy / Tanpa Sikofansi:**  
   Objective 5-domain quantitative friction scoring, rejecting flattery bias and Barnum/Forer cold-reading.
3. **Universal Single Codebase / Satu Basis Kode Universal:**  
   Unified client execution across mobile and desktop web browsers.

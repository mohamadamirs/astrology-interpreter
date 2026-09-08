# Architecture Decision Records (ADRs)

This directory maintains the permanent record of significant architectural decisions made for the **Astrology-Interpreter** platform. Each record documents the context, alternatives considered, decision outcome, and trade-offs.

## Index of Architecture Decision Records

| ADR | Title | Status | Date |
| :---: | :--- | :---: | :---: |
| [**ADR-0001**](./0001-use-python-fastapi-for-astro-engine.md) | Selection of Python (FastAPI) as Core Ephemeris Engine | **Accepted** | 2026-09-08 |
| [**ADR-0002**](./0002-adopt-universal-expo-react-native.md) | Adoption of Universal React Native (Expo) for Mobile & Web | **Accepted** | 2026-09-08 |
| [**ADR-0003**](./0003-offline-timezone-resolution.md) | Offline Geospatial Timezone Resolution via TimeZoneFinder & ZoneInfo | **Accepted** | 2026-09-08 |
| [**ADR-0004**](./0004-dual-zodiac-transformation-architecture.md) | Dual-Zodiac Transformation Architecture (Sidereal & Tropical) | **Accepted** | 2026-09-08 |
| [**ADR-0005**](./0005-exponential-decay-orb-weighting.md) | Continuous Exponential Decay Function for Aspect Orb Weighting | **Accepted** | 2026-09-08 |
| [**ADR-0006**](./0006-hourly-transit-caching-strategy.md) | Hourly Transit Caching Strategy | **Accepted** | 2026-09-08 |

---

## ADR Process & Standards
* All new technical decisions with cross-module impact must be documented using an ADR.
* Format: [Michael Nygard ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record).
* Status progression: `Proposed` $\rightarrow$ `Accepted` $\rightarrow$ `Superseded` (by future ADR).

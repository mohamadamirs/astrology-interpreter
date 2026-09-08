# ADR-0001: Selection of Python (FastAPI) as Core Ephemeris & Calculation Engine

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  
* **Consulted:** Engineering Team  

---

## Context and Problem Statement
The platform requires a backend compute tier capable of performing rigorous, sub-arcsecond celestial mechanics, Julian date conversions, precession matrix transformations (Ayanamsha), and multi-tiered recursive Vimshottari Dasha calculations. The engine must expose high-throughput, low-latency REST endpoints to universal client applications.

We evaluated three potential technology ecosystems:
1. **Python (FastAPI + PyEphem / Swiss Ephemeris)**
2. **Node.js / TypeScript (astronomy-engine / native C++ addons)**
3. **Go (Golang native astronomical ports)**

## Decision Outcome
Chosen option: **Python with FastAPI**, because:
1. **Astronomical Ecosystem Maturity:** Python possesses the most battle-tested astronomical and ephemeris libraries (`ephem`, `pyswisseph`, `skyfield`), officially maintained and verified against NASA JPL Horizons vectors.
2. **Asynchronous Throughput:** FastAPI built on Starlette and Uvicorn provides ASGI asynchronous I/O capabilities comparable to Node.js while retaining Python's native numeric libraries.
3. **Automated Strict Contracts:** Native integration with Pydantic v2 allows compile-time schema validation and automatic OpenAPI 3.1 contract generation.

## Alternatives Considered

### Alternative A: Node.js / TypeScript
* *Pros:* Single-language stack across frontend (React Native) and backend.
* *Cons:* Ephemeris libraries in pure JavaScript (`astronomy-engine`, `sweph-js`) either lack full Vedic divisional support (Nakshatra Sub-Lord arcs, KP ayanamsha) or rely on brittle C++ node-gyp bindings prone to build failures across container environments.

### Alternative B: Go (Golang)
* *Pros:* Exceptional single-binary deployment and raw execution speed.
* *Cons:* Lacks a mature, community-audited port of the Swiss Ephemeris. Implementing IAU precession polynomials and planetary perturbation series from scratch introduces high engineering risk and verification overhead.

## Consequences

### Positive
* Sub-arcsecond calculation accuracy verified directly against benchmark JPL vectors.
* Rapid development of mathematical models using Python's expressive syntax and rich scientific toolchain.
* Strict type-safety and contract enforcement via Pydantic.

### Negative / Trade-offs
* Multi-language repository (Python backend, TypeScript frontend) requiring separate CI linting and dependency management pipelines.
* Python runtime memory footprint is higher than compiled languages like Go/Rust (mitigated via containerized horizontal scaling).

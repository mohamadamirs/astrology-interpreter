# Technical Design Document (TDD) Suite

Welcome to the technical design documentation for the **Astrology-Interpreter Engine & Universal Platform**. This suite is structured in modular, standalone documents following modern enterprise engineering standards:

---

## TDD Folder Structure

```text
docs/en/tdd/
├── 01_system_architecture.md                     # Part 1: Topology, Components, Clean Architecture, Monorepo
├── 02_sequence_diagrams/                         # Part 2: Sequence Diagrams (1 File per Interaction Flow)
│   ├── INDEX.md
│   ├── 01_natal_calculation_and_rectification.md # SD-01: Ingestion & Birth Time Rectifier Slider
│   ├── 02_transit_and_aspect_hit_scanner.md      # SD-02: Time-Travel Transit & Aspect Hit Scanner
│   ├── 03_smart_transit_alerts.md               # SD-03: Critical Transit Push Alerts Evaluation
│   ├── 04_multi_archetype_compatibility.md       # SD-04: Romance/Friend/Coworker Synastry & Strangers
│   ├── 05_rag_chatbot_doctrine.md               # SD-05: Hallucination-Free RAG Classical AI Chatbot
│   └── 06_empirical_journal_and_share.md         # SD-06: Event Journal Logging & Chart Export
├── 03_adr/                                       # Part 3: Architecture Decision Records
│   ├── INDEX.md
│   ├── 0001-use-python-fastapi-for-astro-engine.md
│   ├── 0002-adopt-universal-expo-react-native.md
│   ├── 0003-offline-timezone-resolution.md
│   ├── 0004-dual-zodiac-transformation-architecture.md
│   ├── 0005-exponential-decay-orb-weighting.md
│   ├── 0006-hourly-transit-caching-strategy.md
│   ├── 0007-rag-architecture-and-classical-doctrine-vector-store.md
│   └── 0008-privacy-controls-and-ghost-mode.md
├── 04_failure_handling.md                        # Part 4: Fault Tolerance, Graceful Degradation & Healing
└── 05_scalability.md                             # Part 5: 3-Tier Caching, DB Partitioning, HPA & Concurrency
```

---

## Quick Navigation Index

1. **[01. System Architecture](file:///root/astrology-interpreter/docs/en/tdd/01_system_architecture.md):** Strict determinism, dual-core ecliptic decoupling, 4-tier system topology, 9 pure domain engines, and monorepo structure.
2. **[02. Sequence Diagrams](file:///root/astrology-interpreter/docs/en/tdd/02_sequence_diagrams/INDEX.md):** 6 deep interaction sequence flows, participant breakdown, edge-case mitigation, and payload data contracts.
3. **[03. Architecture Decision Records (ADR)](file:///root/astrology-interpreter/docs/en/tdd/03_adr/INDEX.md):** 8 foundational architectural decision records governing tech stack selection and mathematical algorithms.
4. **[04. Failure Handling](file:///root/astrology-interpreter/docs/en/tdd/04_failure_handling.md):** Comprehensive failure taxonomy, polar coordinate singularities, DST edge-cases, fail-safe bypasses, and disaster recovery.
5. **[05. Scalability & Performance](file:///root/astrology-interpreter/docs/en/tdd/05_scalability.md):** Compute profiling, 3-tier caching (In-process LRU, Redis Hourly, TanStack Query), stateless pod autoscaling, and time-range table partitioning.

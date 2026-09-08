# ADR-0002: Adoption of Universal React Native (Expo) for Mobile and Web Client

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  

---

## Context and Problem Statement
The product roadmap requires immediate availability across Android, iOS, and modern desktop/mobile Web browsers. Maintaining separate codebases (e.g., Swift/Kotlin for mobile and React/Next.js for web) would double engineering overhead, increase feature parity desynchronization, and complicate the maintenance of complex vector chart visualization components.

We evaluated two architectural approaches:
1. **Universal Client via React Native + Expo (`react-native-web`)**
2. **Dual-Codebase Architecture (Next.js for Web + React Native for Mobile)**

## Decision Outcome
Chosen option: **Universal React Native via Expo**, because:
1. **High Code Sharing:** Achieves $\ge 85\%$ code reuse across state management (Zustand), API queries (TanStack Query), business domain types, and UI components.
2. **First-Class Universal Vector Graphics:** Vector chart engines written in `react-native-svg` render deterministically across mobile native canvas and web DOM SVGs without translation layers.
3. **Unified Navigation Paradigm:** Expo Router provides file-based routing supporting deep linking on mobile and standard clean URLs on web.

## Alternatives Considered

### Alternative: Dual Codebase (Next.js + Separate React Native)
* *Pros:* Native SSR/SSG optimization for web SEO.
* *Cons:* Requires duplicate implementation of complex astrological visualizer components (e.g., SVG circular wheels and Vedic square charts). State management and validation hooks must be maintained in duplicate or abstracted into an external monorepo package.

## Consequences

### Positive
* Single PR / commit updates features across Android, iOS, and Web simultaneously.
* Unified developer experience and simplified CI/CD build matrix.
* Reduced time-to-market for MVP.

### Negative / Trade-offs
* Web initial page load is client-side rendered (SPA), which requires prerendering or static optimization if strict SEO indexation is prioritized post-MVP.
* Map integration requires platform-specific branching (`react-native-maps` on mobile vs Leaflet/WebMap on web).

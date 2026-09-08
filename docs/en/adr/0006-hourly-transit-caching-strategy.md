# ADR-0006: Hourly Transit Caching Strategy

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  

---

## Context and Problem Statement
Real-time transit calculations are demanded every time an active user opens the dashboard. Planetary positions in the solar system change continuously; however, the rate of change varies widely:
* Outer planets (Jupiter, Saturn, Uranus, Neptune, Pluto) move $< 0.01^\circ$ per hour.
* Inner planets (Sun, Mercury, Venus, Mars) move $\approx 0.04^\circ$ per hour.
* The Moon moves fastest, at $\approx 0.55^\circ$ per hour ($\approx 0.009^\circ$ per minute).

Recalculating 10 planetary bodies and cross-comparing all mutual aspect angles on every inbound HTTP request creates redundant CPU load and scales poorly under concurrent traffic.

## Decision Outcome
Chosen option: **Hourly Discrete Bucketing with In-Memory & Database Caching**, because:
1. **Bounded Error Margin:** Within a 1-hour window, the maximum angular drift across the entire celestial sphere is $\le 0.55^\circ$ (Moon only) and $\le 0.04^\circ$ for all other bodies. This drift is well within acceptable tolerance for daily transit barometer evaluations.
2. **Deterministic Cache Key:** Truncating timestamps to `YYYY-MM-DD-HH:00:00Z` provides a deterministic primary key (`timestamp_hour_utc`, `ayanamsha_system`).
3. **Sub-15ms Latency:** Serving transit coordinates from memory/PostgreSQL cache drops API response latency from $120\text{ ms}$ to $< 15\text{ ms}$.

## Consequences

### Positive
* Up to $95\%$ reduction in ephemeris CPU compute cycles during high-traffic windows.
* Deterministic cache invalidation and simple background cron pre-computation.

### Negative / Trade-offs
* For users demanding sub-minute Moon ingress timing, a dedicated bypass flag (`?exact=true`) must be provided to force instantaneous real-time computation.

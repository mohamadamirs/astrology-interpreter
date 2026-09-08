# ADR-0003: Offline Geospatial Timezone Resolution via TimeZoneFinder & ZoneInfo

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  

---

## Context and Problem Statement
Astrological birth chart calculation fundamentally requires normalizing civil local birth time to astronomical Coordinated Universal Time (UTC). Converting arbitrary geographic coordinates (Latitude, Longitude) into an official IANA Timezone string (e.g., `Asia/Jakarta`, `America/New_York`) is traditionally achieved via external web APIs (e.g., Google Maps Time Zone API, GeoNames).

External network lookups introduce critical vulnerabilities:
1. **Network Latency & Outage Risk:** Each chart calculation is blocked by external HTTP round-trips ($150\text{ ms} - 500\text{ ms}$).
2. **Operational Cost & Metering Limits:** Rate limits and recurring billing per API call.
3. **Privacy Exposure:** Transmitting user birth coordinates to third-party providers.

## Decision Outcome
Chosen option: **In-Process Offline Resolution via `timezonefinder` and Python `zoneinfo`**, because:
1. **Zero Runtime Network I/O:** Polygon-based spatial indexing resolves coordinate-to-timezone lookups locally in memory within $\le 10\text{ ms}$.
2. **Historical Accuracy:** Pairing the resolved IANA string with Python's standard `zoneinfo` (backed by the official IANA tz database) accurately accounts for historical Daylight Saving Time (DST) switches and territorial offset changes back to 1900.
3. **Absolute Privacy:** Geographic coordinates never leave the application host environment.

## Alternatives Considered

### Alternative: Google Maps Time Zone API
* *Pros:* High maintenance cadence by Google.
* *Cons:* Requires paid Google Cloud billing, network latency, and strict API quota throttling.

## Consequences

### Positive
* Sub-10ms instantaneous timezone resolution.
* Zero external operational dependencies and zero API billing cost.
* Complete compliance with data privacy mandates.

### Negative / Trade-offs
* Increases container image size by $\sim 45\text{ MB}$ to host the pre-compiled binary timezone polygon dataset.
* Requires periodic updates of `timezonefinder` and tzdata packages when governments alter timezone boundaries.

# ADR-0008: Privacy Controls, Birth Data Masking, and Ghost Mode

* **Status:** Accepted  
* **Date:** 2026-09-08  

## Context & Problem Statement
Exact birth timestamps and GPS coordinates represent sensitive personal data. Social capabilities, such as Nearby user discovery and Stranger profile compatibility, could inadvertently leak user locations or exact birth details. Concurrently, the user explicitly mandated that for stranger profiles, all analytical dimensions and compatibility metrics must be fully computed and displayed without omission.

Evaluated options:
1. **Truncated Compatibility (Reduced Dimensions):** Omitting houses or specific aspects for strangers. Rejected per explicit user requirements.
2. **Pure Client-Side Computation:** Carries high risk of exposing raw coordinate inputs via network inspection.
3. **Backend-Isolated Computation with Presentation Masking (Ghost Mode):** Perform complete astronomical calculations on the isolated server, while stripping or fuzzing sensitive identifiers before returning results to the client.

## Decision
Adopt **Backend-Isolated Computation with Presentation Masking**:
1. *Ghost Mode Active:* Completely suspends location beacon broadcasting from Nearby discovery indices.
2. *Data Sanitization:* API filters sensitive birth parameters (`birth_time`, `exact_lat_lon`) from public JSON payloads while returning 100% of the computed compatibility dimensions.
3. *Spatial Jitter:* For public map views, physical coordinates are fuzzed by a minimum radius of 500 meters (*geohash jitter*).

## Consequences
* **Positive:** User privacy is guaranteed without degrading the analytical depth of the compatibility engine.
* **Trade-off:** Demands strict sanitization middleware prior to dispatching responses to client layers.

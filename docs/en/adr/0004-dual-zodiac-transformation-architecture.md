# ADR-0004: Dual-Zodiac Transformation Architecture (Sidereal Default + Tropical Option)

* **Status:** Accepted  
* **Date:** 2026-09-08  
* **Deciders:** Architecture Team  

---

## Context and Problem Statement
Global astrological practitioners are sharply divided into two distinct paradigms:
1. **Western (Tropical / Sayana):** Anchored to the Vernal Equinox ($0^\circ$ Aries = March equinox). Dominates psychological character analysis in Western markets.
2. **Vedic / Eastern (Sidereal / Nirayana):** Anchored to the physical fixed star background via precession offsets (Ayanamsha). Dominates predictive timing systems (Vimshottari Dasha) and planetary dignity scoring.

Building an engine tailored exclusively to one paradigm alienates half the potential global user base or causes algorithmic confusion when applying Dasha timing rules to tropical positions.

## Decision Outcome
Chosen option: **Normalized Dual-Zodiac Architecture with Explicit Ayanamsha Decoupling**, because:
1. **Canonical Apparent Ecliptic Storage:** The ephemeris engine calculates absolute geocentric apparent ecliptic longitudes $[0^\circ, 360^\circ)$ as the baseline truth.
2. **Explicit Transformation Layer:** Tropical positions are derived as $\lambda_{\text{tropical}} = \lambda_{\text{ecliptic}}$. Sidereal positions are derived via explicit subtraction $\lambda_{\text{sidereal}} = (\lambda_{\text{tropical}} - \text{Ayanamsha}(T)) \pmod{360^\circ}$.
3. **Rigid Scope Enforcement:** Vimshottari Dasha calculations and Nakshatra divisions are strictly constrained to the Sidereal dataset to preserve traditional Jyotish mathematical validity, while Western aspect chords can operate across either framework.

## Consequences

### Positive
* Enables seamless client-side toggling between Western and Vedic visual representations without recalculating raw ephemeris data.
* Eliminates calculation errors where Tropical longitudes are erroneously fed into Vedic Nakshatra algorithms.

### Negative / Trade-offs
* API payloads must carry both representations or explicit parameter flags, increasing response JSON payload size by $\sim 30\%$.

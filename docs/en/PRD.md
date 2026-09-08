# Product Requirements Document (PRD) - Master Feature Inventory

This document outlines **the comprehensive feature inventory requested by the user**. It serves as the master feature backlog prior to triaging items into the initial foundation (MVP) versus subsequent phases.

---

## 1. Core Mandates

1. **Zero Tolerance for the Barnum / Forer Effect:**
   * Strict rejection of generic horoscopes, flattery, or ambiguous statements that could apply to anyone.
   * All interpretations must be mathematically objective and grounded in demonstrable celestial causality.
2. **High Precision in Transit Impact Evaluation:**
   * Use highly precise methods to measure the impact of transit positions on the natal chart.

---

## 2. Master Feature Inventory

### Feature 1: Complete Birth Chart Analysis (Dual-Method)
* Comprehensive natal calculations across **two primary traditions**:
  1. **Western Astrology (*Tropical / Sayana*)**
  2. **Indian Astrology (*Vedic / Sidereal*)**

### Feature 2: Dual Visual Chart Rendering
* **Western Format:** 360-degree Circular Wheel with internal geometric aspect connection lines.
* **Indian Format:** Traditional Vedic square charts (*South Indian grid* and/or *North Indian diamond*).
* Raw astronomical data table (exact degree, minute, second, retrograde flag, daily speed).

### Feature 3: Birth Chart Storage
* Computed birth chart data must persist permanently in storage/database, allowing users to save, manage, and retrieve profiles at any time.

### Feature 4: Dynamic Birth Time Adjuster (*Rectification Slider*)
* Interactive minute/hour adjustment slider directly on the chart interface for users with approximate birth times.
* Users can scrub time backward/forward (e.g., $\pm 30$ minutes) and observe instantaneous shifting of Ascendant (Lagna) degrees and house boundaries in real time.

### Feature 5: Time-Traveling Transit Engine
* Bidirectional, dynamic transit exploration:
  * **Today (*Real-time*)**
  * **Past (*Historical events*)**
  * **Future (*Predictive*)**
  * Ability to scrub back and forth across time.
* **Interaction Modes:**
  * **Slider:** Smooth forward/backward time-scrubbing.
  * **Calendar:** Calendar view marking dates with significant active transits.
  * **Key Moment Finder (*Aspect Hit Scanner*):** Automated search tool jumping directly to exact hit dates for critical transits.

### Feature 6: Smart Transit Alerts (Critical Transit Notifications)
* Automated push notifications triggered when exact, tight-orb transits hit sensitive natal points.
* Notifications convey objective astronomical facts and impacted life areas without sensationalism.

### Feature 7: Empirical Astro-Journal (*Event Diary*)
* Diary feature integrated into the transit timeline.
* Users can log real-world events on specific dates to test, validate, and track empirical correlations between planetary movements and lived experiences.

### Feature 8: Share Feature
* Ability for users to share charts and analysis results with others or export them externally.

### Feature 9: Multi-Archetype Compatibility (*Synastry*)
* Compatibility evaluation extends beyond romantic couples to include:
  * **Romantic Partners**
  * **Friends**
  * **Coworkers / Business Partners**
* **Target Profile Ingestion Sources:**
  * Based on **Phone Contacts**.
  * Based on **Nearby Users / Proximity**.
  * Based on **Unknown / Stranger Profiles:** Complete compatibility dimensions and analysis are fully computed and displayed.

### Feature 10: Privacy Controls & Ghost Mode
* Privacy toggle to protect sensitive birth date and time data:
  * Option to enable/disable discovery by nearby users.
  * Option to share compatibility scores without revealing underlying raw birth data to third parties.

### Feature 11: AI Chatbot with RAG (*Retrieval-Augmented Generation*)
* Translates dense raw astronomical data into clear, human-understandable insights.
* RAG grounds responses in authoritative classical texts and user's exact positions to eliminate hallucinations and reject Barnum-style generic statements.

---

## 3. Phasing Note

All 11 items above represent the complete desired feature set. In the next planning stage, these features will be triaged to establish:
* **Phase 1 (Foundation / MVP):** Core features required to make the system functionally testable.
* **Subsequent Phases:** Advanced capabilities to be rolled out incrementally.

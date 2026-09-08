# Product Requirements Document (PRD) - Master Feature Inventory

This document outlines **all requirements and features explicitly requested by the user**. It serves as the master feature inventory prior to prioritizing which components form the initial foundation (MVP) versus subsequent phases.

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
* Comprehensive natal chart calculations across **two primary traditions**:
  1. **Western Astrology (*Tropical / Sayana*)**
  2. **Indian Astrology (*Vedic / Sidereal*)**

### Feature 2: Birth Chart Storage
* Computed birth chart data must persist permanently in storage/database, allowing users to save, manage, and retrieve profiles at any time.

### Feature 3: Time-Traveling Transit Engine
* Bidirectional, dynamic transit exploration:
  * **Today (*Real-time*)**
  * **Past (*Historical events*)**
  * **Future (*Predictive*)**
  * Ability to scrub back and forth across time.
* **Interaction Modes:**
  * **Slider:** Smooth forward/backward time-scrubbing.
  * **Calendar:** Calendar view marking dates with significant active transits.
  * **Key Moment Finder (*Aspect Hit Scanner*):** Automated search tool jumping directly to exact hit dates for critical transits.

### Feature 4: Share Feature
* Ability for users to share charts and analysis results with others or export them externally.

### Feature 5: Multi-Archetype Compatibility (*Synastry*)
* Compatibility evaluation extends beyond romantic couples to include:
  * **Romantic Partners**
  * **Friends**
  * **Coworkers / Business Partners**
* **Target Profile Ingestion Sources:**
  * Based on **Phone Contacts**.
  * Based on **Nearby Users / Proximity**.
  * Based on **Unknown / Stranger Profiles:** Complete compatibility dimensions and analysis are fully computed and displayed.

### Feature 6: AI Chatbot with RAG (*Retrieval-Augmented Generation*)
* To translate dense raw astronomical coordinates, nakshatras, and aspect degrees into clear, human-understandable insights.
* **RAG Role:** Ingests vetted, authoritative astrological texts and grounds them with the user's exact raw data to eliminate hallucinations and avoid Barnum-style generic statements.

---

## 3. Phasing Note

All items above represent the complete desired feature set. In the next planning stage, these features will be triaged to establish:
* **Phase 1 (Foundation / MVP):** Core features required to make the system functionally testable.
* **Subsequent Phases:** Advanced capabilities to be rolled out incrementally.

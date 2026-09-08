# Sequence Diagram 04: Multi-Archetype Compatibility & Stranger Profiles

**Document ID:** SD-ASTRO-004  
**Related Features:** Feature 9 (Multi-Archetype Compatibility), Feature 10 (Privacy Controls & Ghost Mode)  
**Status:** Approved  

---

## 1. Scenario Description

This sequence diagram illustrates the relational compatibility (*synastry*) pipeline between two chart profiles:
1. The user selects one of three distinct relational archetypes: **Romance**, **Friendship**, or **Coworker / Business Partner**.
2. The user ingests a partner profile from Phone Contacts, Nearby Proximity, or an **Unknown / Stranger Profile**.
3. The system enforces **Ghost Mode & Privacy Rules**: if the target profile has Ghost Mode enabled, sensitive birth dates, exact timestamps, and physical addresses are masked. However, **all analytical dimensions and compatibility metrics are calculated and displayed in full without omitting any dimensions** (explicit user requirement).
4. The *CompatibilityEngine* computes inter-chart Western aspects, Vedic Ashta Kuta scores (out of 36 points), and archetype-specific synergy matrices (e.g., Mercury-Saturn focus for coworkers).

---

## 2. System Participants

* **User:** End user initiating the compatibility check.
* **UI_App (Expo React Native):** `CompatibilityMatrix` UI and target profile ingestion selector.
* **API_Gateway (FastAPI):** Endpoint `/api/v1/compatibility/evaluate`.
* **PrivacyMiddleware:** Enforces privacy masking, coordinate fuzzing, and Ghost Mode sanitization.
* **CompatibilityEngine:** Multi-dimensional synastry engine computing composite scores.
* **VedicKutaEngine:** Computes traditional 8 Kutas (Varna, Vashya, Tara, Yoni, Graha Maitri, Gana, Bhakoot, Nadi).
* **WesternSynastryEngine:** Computes inter-chart planetary aspect chords with continuous exponential decay weighting.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as UI_App (Compatibility View)
    participant API as API_Gateway (FastAPI)
    participant Sec as PrivacyMiddleware
    participant Compat as CompatibilityEngine
    participant Kuta as VedicKutaEngine
    participant Syn as WesternSynastryEngine

    User->>UI: Select Archetype: "Coworker" & Source: "Stranger Profile (City: Bandung)"
    User->>UI: Submit Target Profile / Tap Nearby Profile
    UI->>API: POST /api/v1/compatibility/evaluate {user_chart_id, target_profile, archetype: "COWORKER"}
    activate API

    API->>Sec: apply_privacy_and_ghost_rules(target_profile)
    activate Sec
    Note over Sec: Inspect target Ghost Mode status.<br/>If Ghost Mode Active: Mask sensitive birth timestamp and coordinates.<br/>DO NOT REDUCE DIMENSIONS: All raw astronomical coordinates passed to internal Engine.
    Sec-->>API: sanitized_target_metadata
    deactivate Sec

    par Vedic Kuta Evaluation (Moon & Nakshatra)
        API->>Kuta: compute_ashta_kuta(user_vedic_chart, target_vedic_chart)
        activate Kuta
        Note over Kuta: Calculate 8 Kutas (Varna, Vashya, Tara, Yoni, Maitri, Gana, Bhakoot, Nadi)<br/>Baseline score out of 36 points
        Kuta-->>API: {kuta_score: 28, kuta_breakdown: {...}}
        deactivate Kuta
    and Western Inter-Aspect Synastry Evaluation
        API->>Syn: compute_inter_aspects(user_planets, target_planets, archetype="COWORKER")
        activate Syn
        Note over Syn: Calculate inter-aspects User A vs Target B:<br/>1. Coworker Focus: Mercury-Saturn, Mars-Sun, Houses 6/10<br/>2. Apply exponential decay weighting $W(\delta)$
        Syn-->>API: {inter_aspects[], tension_points[], synergy_points[]}
        deactivate Syn
    end

    API->>Compat: synthesize_archetype_score(kuta_result, synastry_result, archetype="COWORKER")
    activate Compat
    Note over Compat: Apply Coworker domain multipliers:<br/>Communication Flow (40%), Work Ethic & Discipline (35%), Leadership Balance (25%)<br/>Synthesize actionable advice devoid of generic flattery
    Compat-->>API: full_compatibility_report
    deactivate Compat

    API-->>UI: HTTP 200 OK: FullCompatibilityResponse
    deactivate API

    UI->>UI: Render Compatibility Dimensional Radar & Synergy/Friction Cards
    UI-->>User: Display Comprehensive Compatibility Report (All Dimensions Visible)
```

---

## 4. Edge Case Handling

| Edge Case | Risk | Mitigation Mechanism |
| :--- | :--- | :--- |
| **Stranger Profile with Unknown Exact Time** | Ascendant and house boundaries for the partner cannot be definitively established. | Fall back to Solar/Lunar house frameworks (*Surya/Chandra Lagna*) as secondary house references, with transparent diagnostic messaging indicating moon-derived houses. |
| **Location Data Exploitation (*Stalking*)** | Malicious users weaponizing Nearby discovery to track precise user coordinates. | Physical GPS coordinates are strictly fuzzed (*geohash jitter*) to a minimum 500-meter radius; exact street addresses are never broadcast. |
| **Romantic Archetype Bias Bleeding into Coworkers** | Algorithm surfacing romantic advice in a professional workplace context. | Isolate archetype weighting logic: in the Coworker archetype, Venus-Mars romantic sexual tension vectors are weighted to zero, focusing purely on Mercury-Saturn-Mars-Jupiter collaboration dynamics. |

---

## 5. Contract Data Structure

### Request: `POST /api/v1/compatibility/evaluate`
```json
{
  "user_chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "target_type": "STRANGER",
  "target_payload": {
    "city_name": "Bandung",
    "approximate_date": "2005-03-15",
    "is_ghost_mode": true
  },
  "archetype": "COWORKER"
}
```

### Response: `HTTP 200 OK`
```json
{
  "status": "success",
  "archetype": "COWORKER",
  "profile_display": {
    "alias": "Anonymous User (Bandung)",
    "birth_details_masked": true
  },
  "overall_score": 78,
  "dimensions": {
    "communication_flow": {"score": 85, "verdict": "High Rapport (Mercury Trine Mercury)"},
    "work_ethic_discipline": {"score": 72, "verdict": "Structured (Saturn Sextile Mars)"},
    "ego_and_leadership": {"score": 68, "verdict": "Moderate Friction (Sun Square Mars)"}
  },
  "vedic_ashta_kuta": {
    "total_points": 26,
    "max_points": 36,
    "graha_maitri": 5,
    "gana_kuta": 6
  },
  "actionable_guidance": "Communication flow is highly conceptual and agile. Clearly delineate task ownership and leadership responsibilities to avoid friction under high-pressure delivery deadlines."
}
```

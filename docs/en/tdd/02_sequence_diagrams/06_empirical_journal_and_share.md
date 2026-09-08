# Sequence Diagram 06: Empirical Journal Logging & Share Feature

**Document ID:** SD-ASTRO-006  
**Related Features:** Feature 7 (Empirical Astro-Journal), Feature 8 (Share Feature)  
**Status:** Approved  

---

## 1. Scenario Description

This sequence diagram illustrates personal event logging anchored to celestial mechanics:
1. The user logs a real-world lived event on a specific date and time (e.g. acute physical fatigue, promotion, major interpersonal friction).
2. The system captures and locks an astronomical snapshot (transit positions, active aspects with exponential weights $W(\delta)$, and current Dasha hierarchy) at that exact moment.
3. The journal entry persists permanently linked to the transit timeline.
4. The user exports or shares high-resolution chart graphics or transit cards (PNG/SVG or secure link).

---

## 2. System Participants

* **User:** End user recording empirical observations or sharing charts.
* **UI_App (Expo React Native):** Journal Screen & native Share action sheet.
* **API_Gateway (FastAPI):** Endpoints `/api/v1/journal/log` and `/api/v1/share/export`.
* **TransitService:** Astronomical provider computing sky snapshots and active aspect weights.
* **JournalRepository (Database):** PostgreSQL / SQLite `journal_entries` table.
* **ShareExportService:** High-resolution SVG/PNG renderer and deep-link generator.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as UI_App (Journal Screen)
    participant API as API_Gateway (FastAPI)
    participant Transit as TransitService
    participant DB as JournalRepository (DB)
    participant Share as ShareExportService

    %% Scenario A: Empirical Journal Logging
    User->>UI: Submit Event Note ("2026-08-14: Extreme physical fatigue and mandatory team restructuring")
    UI->>API: POST /api/v1/journal/log {chart_id: "uuid-1234", event_date: "2026-08-14T09:00:00Z", note: "..."}
    activate API

    API->>Transit: capture_sky_snapshot(chart_id, "2026-08-14T09:00:00Z")
    activate Transit
    Note over Transit: Lock transit coordinates at timestamp:<br/>1. Transit Saturn Opposition Natal Sun (orb 0.04°)<br/>2. Active Dasha: Saturn - Saturn
    Transit-->>API: sky_snapshot_json {active_aspects[], dasha_active, dominant_domain: "Career/Somatic"}
    deactivate Transit

    API->>DB: INSERT INTO journal_entries (chart_id, event_utc, note_text, sky_snapshot)
    activate DB
    DB-->>API: {entry_id: "entry-8899", created_at: "2026-09-08T09:51:00Z"}
    deactivate DB

    API-->>UI: HTTP 201 Created: {status: "success", entry_id: "entry-8899", sky_snapshot}
    deactivate API

    UI->>UI: Anchor Journal Card onto Interactive Transit Timeline
    UI-->>User: Display Journal Entry Linked to Astronomical Snapshot

    %% Scenario B: Share Feature
    User->>UI: Tap "Share Chart / Transit Summary" (Choose Format: PNG/SVG)
    UI->>API: POST /api/v1/share/export {chart_id: "uuid-1234", export_type: "IMAGE_CARD", include_details: true}
    activate API

    API->>Share: render_high_res_visual_card(chart_data)
    activate Share
    Note over Share: Convert 360° zodiac wheel & transit summary<br/>into 300 DPI PNG or vector SVG asset
    Share-->>API: {media_url: "https://storage.astro.io/exports/card-99.png", share_code: "astro-xyz"}
    deactivate Share

    API-->>UI: HTTP 200 OK: {download_url, share_link}
    deactivate API

    UI->>UI: Open Native OS Share Sheet (WhatsApp, Save Image, AirDrop)
    UI-->>User: Visual Chart Successfully Exported
```

---

## 4. Edge Case Handling

| Edge Case | Risk | Mitigation Mechanism |
| :--- | :--- | :--- |
| **Historical Childhood Event Logging (e.g., Year 1995)** | Missing hourly cache for distant past dates. | *On-Demand Ephemeris Execution*: Seamlessly invokes `pyswisseph` directly to compute past coordinates on the fly. |
| **Overly Large File Export** | Failure during sharing over messaging platforms. | Image optimization pipeline enforcing aggressive PNG palette quantization (target $\le 2\text{ MB}$ per card). |
| **Private Journal Data Exposure** | Sensitive personal diary notes leaking when sharing charts publicly. | Public export templates strictly exclude freeform user journal text by default, exposing only pure celestial geometry and transit metrics. |

---

## 5. Contract Data Structure

### Request: `POST /api/v1/journal/log`
```json
{
  "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "event_date": "2026-08-14T09:00:00Z",
  "note": "Experienced acute physical exhaustion and major structural demands at work.",
  "subjective_tags": ["Work", "Fatigue", "Restructure"]
}
```

### Response: `HTTP 201 Created`
```json
{
  "status": "success",
  "entry_id": "8b9e6c2d-88f1-432a-bc91-912837264819",
  "anchored_astronomy": {
    "target_utc": "2026-08-14T09:00:00Z",
    "primary_transit": "Saturn Opposition Sun (Orb 0.04°)",
    "active_dasha": "Saturn-Saturn",
    "affected_domains": ["Career/Situational", "Somatic/Physiological"]
  }
}
```

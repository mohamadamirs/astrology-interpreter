# Sequence Diagram 03: Evaluation & Dispatch of Smart Transit Alerts

**Document ID:** SD-ASTRO-003  
**Related Features:** Feature 6 (Smart Transit Alerts / Critical Transit Notifications)  
**Status:** Approved  

---

## 1. Scenario Description

This sequence diagram illustrates the automated background evaluation pipeline for critical transit notifications:
1. A periodic background worker triggers daily scans across registered active users.
2. The *TransitEngine* detects transits forming extremely tight orbs ($\le 0.25^\circ$) against sensitive natal chart points (Sun, Moon, Ascendant, or active Dasha lords).
3. The system formats an objective, astronomy-grounded notification devoid of sensationalist platitudes.
4. Notifications are dispatched to user devices via push gateways (APNs / FCM).

---

## 2. System Participants

* **AlertScheduler (Daily Cron / Celery Beat):** Periodic worker kicking off daily batch scans.
* **AlertEvaluationService:** Orchestrator assessing user alert rules and active chart transits.
* **AlertRepository (Database):** Persistent store providing active user rules and push tokens.
* **EphemerisService & AspectEngine:** Astronomical services providing transit coordinates and orb matching.
* **NotificationFormatter:** Text synthesizer producing objective, anti-sensationalist copy.
* **PushGateway (FCM / APNs):** Push service delivering notifications to mobile devices.
* **UI_App (Mobile Device):** Client mobile application receiving push payloads.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    participant Sched as AlertScheduler (Daily Cron)
    participant Worker as AlertEvaluationService
    participant DB as AlertRepository (DB)
    participant Engine as Ephemeris & AspectEngine
    participant Fmt as NotificationFormatter
    participant Push as PushGateway (FCM / APNs)
    participant Client as UI_App (User Mobile)

    %% Daily Background Trigger
    Sched->>Worker: Trigger daily_transit_alert_scan(target_date)
    activate Worker

    Worker->>DB: get_active_alert_subscriptions()
    DB-->>Worker: list_of_users_with_rules[] (user_id, natal_chart_id, fcm_token, orb_threshold)

    loop For Each Registered User
        Worker->>Engine: evaluate_critical_transits(natal_chart_id, target_date, orb_threshold=0.25)
        activate Engine
        Note over Engine: Check transits to sensitive points:<br/>Ascendant, Midheaven, Sun, Moon & active Dasha lord<br/>Filter transits with orb <= 0.25 deg
        Engine-->>Worker: detected_critical_transits[]
        deactivate Engine

        alt Critical Transit Detected
            Worker->>Fmt: format_objective_alert(detected_transits)
            activate Fmt
            Note over Fmt: Compose objective astronomical copy:<br/>State bodies, exact orb & affected life domains.<br/>Strictly anti-sensationalist!
            Fmt-->>Worker: alert_payload {title, body, data: {chart_id, transit_event}}
            deactivate Fmt

            Worker->>Push: send_notification(fcm_token, alert_payload)
            activate Push
            Push->>Client: Deliver Push Notification ("Exact Transit: Saturn Opposition Sun...")
            Push-->>Worker: delivery_status (SUCCESS / FAILED)
            deactivate Push

            Worker->>DB: log_alert_delivery(user_id, alert_payload, status)
        else No Critical Transits
            Note over Worker: Skip user; zero notification spam
        end
    end

    Worker-->>Sched: batch_completed {total_processed, total_sent}
    deactivate Worker

    %% Mobile Device Interaction
    Client->>Client: User Taps Notification
    Client->>Client: Open App & Deep Link to Transit Detail View
```

---

## 4. Edge Case Handling

| Edge Case | Risk | Mitigation Mechanism |
| :--- | :--- | :--- |
| **Expired Device Push Tokens** | Persistent delivery failures via FCM/APNs. | Worker catches `UNREGISTERED` / `INVALID_TOKEN` errors and automatically deactivates stale tokens in the database. |
| **Notification Flooding (*Alert Fatigue*)** | User receives multiple alerts in a single day. | *Notification Rate Limiting*: Enforce a hard cap of 1 primary aggregated digest per 24-hour cycle per user. |
| **Timezone Shifts for Alerts** | Notifications delivered at inconvenient local times (e.g. midnight). | Schedule dispatches localized to each user recorded `iana_timezone` (e.g., delivered at 07:00 local time). |

---

## 5. Notification Contract Payload

```json
{
  "to": "fcm_token_device_abc123",
  "notification": {
    "title": "Critical Transit: Saturn Opposition Sun",
    "body": "Exact culmination (orb 0.04°). Focus themes: Structural discipline, physiological fatigue boundaries, and work reorganization."
  },
  "data": {
    "type": "TRANSIT_ALERT",
    "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
    "transit_planet": "Saturn",
    "natal_point": "Sun",
    "aspect_type": "opposition",
    "exact_orb": 0.041,
    "timestamp_utc": "2026-08-14T03:22:15Z"
  }
}
```

# Sequence Diagram 02: Mesin Transit Bolak-Balik Waktu & Aspect Hit Scanner

**ID Dokumen:** SD-ASTRO-002  
**Fitur Terkait:** Fitur 5 (Mesin Transit Bolak-Balik Waktu: Slider, Kalender, Aspect Hit Scanner)  
**Status:** Disetujui  

---

## 1. Deskripsi Skenario

Diagram ini memodelkan dua interaksi utama pada mesin transit:
1. **Navigasi Waktu Bolak-Balik (Slider & Kalender):** Pengguna menggeser tanggal/jam ke masa lalu atau masa depan. Sistem mengecek *Hourly Discrete Transit Cache* (ADR-0006) untuk mengembalikan koordinat transit secara instan tanpa re-komputasi CPU berlebih, lalu membandingkannya terhadap bagan natal pengguna menggunakan fungsi peluruhan eksponensial (ADR-0005).
2. **Pencari Momen Kritis (*Aspect Hit Scanner*):** Pengguna memilih target transit spesifik (misal: *"Saturnus Oposisi Matahari Natal"*). Sistem mengeksekusi algoritma pencarian akar numerik (*root-finding bisection / Newton-Raphson*) untuk melacak tanggal dan jam eksak saat orb bernilai $0.000^\circ$, lalu membawa linimasa antarmuka langsung ke momen puncak tersebut.

---

## 2. Partisipan Sistem

* **Pengguna (User):** Aktor akhir yang menavigasi linimasa waktu atau mencari momen transit.
* **UI_App (Expo React Native):** Komponen `TransitController` (Slider harian, Kalender heatmap, Form Scanner).
* **API_Gateway (FastAPI):** Endpoint `/api/v1/transit/timeline` dan `/api/v1/transit/scan-hit`.
* **TransitCacheService:** Lapisan in-memory/Redis atau tabel DB yang menyimpan koordinat langit per jam diskrit.
* **EphemerisCore:** Solver astronomis `pyswisseph` yang menghitung bujur ekliptika dan kecepatan sesaat.
* **AspectScoringEngine:** Algoritma pembobotan orb eksponensial $W(\delta) = 10.0 	imes \exp(-1.4 	imes \delta)$.
* **NumericalRootSolver:** Algoritma interpolasi bisection untuk mencari tanggal puncak orb minimum.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User as Pengguna
    participant UI as UI_App (Transit View)
    participant API as API_Gateway (FastAPI)
    participant Cache as TransitCacheService (In-Memory/Redis)
    participant Ephem as EphemerisCore
    participant Score as AspectScoringEngine
    participant Solver as NumericalRootSolver

    %% Skenario A: Navigasi Linimasa Transit (Slider / Kalender)
    User->>UI: Geser Slider Waktu ke Tanggal Target (e.g. 2026-11-15 14:00 UTC)
    UI->>API: GET /api/v1/transit/timeline?chart_id=uuid-1234&target_utc=2026-11-15T14:00:00Z
    activate API

    API->>Cache: get_discrete_ephemeris(2026-11-15, hour=14)
    activate Cache
    alt Cache Hit (Data Jam Diskrit Tersedia)
        Cache-->>API: cached_planetary_positions[]
    else Cache Miss (Belum Dihitung)
        Cache-->>API: null
        API->>Ephem: compute_planetary_positions(target_julian_day)
        Ephem-->>API: calculated_positions[]
        API->>Cache: store_discrete_ephemeris(2026-11-15, hour=14, calculated_positions)
    end
    deactivate Cache

    API->>Score: calculate_transit_to_natal_aspects(natal_chart, transit_positions)
    activate Score
    Note over Score: Hitung selisih sudut $\delta$ untuk tiap pasangan planet<br/>Terapkan rumus: $W(\delta) = 10 	imes \exp(-1.4 	imes \delta)$<br/>Identifikasi aspek aktif (orb <= 6 derajat)
    Score-->>API: active_aspects_list[] with exact_orbs and weights
    deactivate Score

    API-->>UI: HTTP 200 OK: {transit_positions, active_aspects, dominant_themes}
    deactivate API

    UI->>UI: Render Pergerakan Posisi Planet pada Roda & List Aspek
    UI-->>User: Tampilan Posisi Langit & Pengaruh Transit Hari Terpilih

    %% Skenario B: Aspect Hit Scanner (Pencari Momen Kritis)
    User->>UI: Pilih Menu "Hit Scanner" (Target: "Saturn Opposition Sun", Rentang: 2026-2027)
    UI->>API: POST /api/v1/transit/scan-hit {natal_planet: "Sun", transit_planet: "Saturn", aspect_type: "opposition", start_year: 2026, end_year: 2027}
    activate API

    API->>Solver: scan_exact_aspect_hits("Saturn", "Sun", 180.0, 2026_01_01, 2027_12_31)
    activate Solver
    Note over Solver: 1. Coarse Scan: Sampling koordinat per 5 hari<br/>2. Deteksi pergantian tanda selisih sudut (zero-crossing)<br/>3. Fine Scan: Bisection / Newton-Raphson hingga akurasi orb < 0.001 derajat
    Solver->>Ephem: compute_positions_at_epoch(interpolated_jd)
    Ephem-->>Solver: precise_positions
    Solver-->>API: list_of_exact_hits [ {exact_utc: "2026-08-14T03:22:15Z", peak_orb: 0.0001, is_retrograde: true} ]
    deactivate Solver

    API-->>UI: HTTP 200 OK: {hits: [...], message: "Found 1 exact hit"}
    deactivate API

    UI-->>User: Tampilkan Daftar Tanggal Puncak Transit Eksak
    User->>UI: Klik Salah Satu Tanggal Hasil Hit
    UI->>UI: Lompatkan Slider Linimasa ke Tanggal Tersebut
    UI-->>User: Visualisasikan Konfigurasi Langit Eksak pada Tanggal Puncak
```

---

## 4. Penanganan Kasus Khusus (*Edge Cases*)

| Kasus Khusus | Risiko | Mekanisme Penanganan |
| :--- | :--- | :--- |
| **Triple Hit akibat Periode Retrograde** | Planet luar (Saturnus/Jupiter) melewati titik eksak 3 kali (direct $ightarrow$ retro $ightarrow$ direct). | Solver mendeteksi pergantian arah kecepatan sesaat (*speed sign flip*) dan mengelompokkan 3 tanggal hit ke dalam satu siklus *"Tri-Hit Transit Cycle"*. |
| **Pencarian Rentang Waktu Terlalu Panjang (>50 tahun)** | Timeout server akibat kalkulasi loop panjang. | Batasi kueri scanner maksimal rentang 5 tahun per request dengan penanda paginasi (*pagination token*). |
| **Ketidaksinambungan Sudut ($360^\circ \leftrightarrow 0^\circ$)** | Selisih sudut melompat dari $359.9^\circ$ ke $0.1^\circ$ (*modular wrap-around*). | Gunakan fungsi selisih sudut sirkular minimum: $\Delta	heta = \min(|	heta_1 - 	heta_2|, 360^\circ - |	heta_1 - 	heta_2|)$. |

---

## 5. Struktur Kontrak Data (Contoh Ringkas)

### Request: `POST /api/v1/transit/scan-hit`
```json
{
  "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "transit_body": "Saturn",
  "natal_body": "Sun",
  "aspect_angle": 180.0,
  "date_range": {
    "start_utc": "2026-01-01T00:00:00Z",
    "end_utc": "2027-12-31T23:59:59Z"
  }
}
```

### Response: `HTTP 200 OK`
```json
{
  "status": "success",
  "total_hits_found": 1,
  "hits": [
    {
      "hit_number": 1,
      "exact_utc": "2026-08-14T03:22:15Z",
      "transit_body_longitude": 335.1204,
      "natal_body_longitude": 155.1200,
      "exact_aspect_angle": 180.0004,
      "orb": 0.0004,
      "is_retrograde": true,
      "weight_score": 10.0,
      "affected_domains": ["Career/Situational", "Mental/Cognitive"]
    }
  ]
}
```

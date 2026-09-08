# Spesifikasi REST API

**Base URL:** `/api/v1` | **Content-Type:** `application/json`

---

## 1. Format Envelope Global

### 1.1 Respon Sukses (HTTP 200)
```json
{
  "success": true,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "data": { ... }
}
```

### 1.2 Respon Error (HTTP 4xx / 5xx)
```json
{
  "success": false,
  "timestamp_utc": "2026-09-08T07:25:00Z",
  "error": {
    "code": "ERR_INVALID_COORDINATES",
    "message": "Latitude harus berada di antara -90.0 dan 90.0 derajat.",
    "field": "latitude"
  }
}
```

---

## 2. Titik Akhir (Endpoints)

### 2.1 `POST /geo/resolve-timezone`
Memetakan koordinat ke zona waktu IANA dan offset UTC untuk tanggal sipil tertentu.

* **Request:**
```json
{
  "latitude": -6.8700,
  "longitude": 109.0400,
  "civil_date": "2007-08-29",
  "civil_time": "06:40:00"
}
```
* **Response (200):**
```json
{
  "success": true,
  "data": {
    "iana_timezone": "Asia/Jakarta",
    "utc_offset_hours": 7.0,
    "is_dst_active": false,
    "calculated_utc_timestamp": "2007-08-28T23:40:00Z"
  }
}
```

### 2.2 `POST /chart/natal`
Menghitung posisi planet zodiak ganda, Lagna, Nakshatra, dan siklus Vimshottari Dasha.

* **Request:**
```json
{
  "birth_date": "2007-08-29",
  "birth_time": "06:40:00",
  "latitude": -6.8700,
  "longitude": 109.0400,
  "ayanamsha": "lahiri",
  "house_system": "whole_sign"
}
```
* **Response (200 - Ringkasan):**
```json
{
  "success": true,
  "data": {
    "metadata": {
      "utc_birth_time": "2007-08-28T23:40:00Z",
      "resolved_timezone": "Asia/Jakarta",
      "ayanamsha_deg": 23.9641
    },
    "angles": {
      "ascendant_lagna": {
        "sidereal_deg": 145.5365,
        "formatted": "Leo 25°32'11\"",
        "nakshatra": "Purva Phalguni",
        "pada": 4,
        "sub_lord": "Mercury"
      }
    },
    "planets": {
      "sun": { "formatted": "Leo 11°13'05\"", "dignity": "Moolatrikona", "is_retrograde": false },
      "moon": { "formatted": "Aquarius 18°31'04\"", "nakshatra": "Shatabhisha", "pada": 4 }
    },
    "vimshottari_dasha": {
      "active_cycle": { "md": "Saturn", "ad": "Saturn", "pd": "Ketu", "sd": "Saturn" },
      "relationship_md_ad": "Self-Reinforcing"
    }
  }
}
```

### 2.3 `GET /transits/current`
Mengembalikan posisi benda langit saat ini (Di-cache per jam).
* **Query:** `ayanamsha=lahiri`
* **Response (200):** Peta planet lengkap dengan zodiak, derajat, kecepatan, dan status retrograde.

### 2.4 `POST /interpret/dynamic`
Mengevaluasi aspek transit ke natal dan menghasilkan skor 5 domain.
* **Request:** `{"natal_chart_id": "UUID", "target_timestamp_utc": "ISO8601"}`
* **Response (200):**
  * `top_weighted_aspects`: Daftar aspek aktif beserta orb dan bobot eksak.
  * `domain_barometer`: Skor integer & status untuk `mental_cognitive`, `emotional_psychological`, `career_situational`, `interpersonal_relational`, `physiological_vitality`.
  * `unvarnished_verdict`: Diagnosa operasional langsung tanpa pemanis kata.

---

## 3. Daftar Kode Error

| Kode Error | Status HTTP | Penyebab |
| :--- | :---: | :--- |
| `ERR_INVALID_COORDINATES` | 422 | Lat $\notin [-90, 90]$ atau Lon $\notin [-180, 180]$. |
| `ERR_DATE_OUT_OF_BOUNDS` | 400 | Tanggal di luar rentang efemeris ($1800 - 2100\text{ M}$). |
| `ERR_AYANAMSHA_UNSUPPORTED` | 400 | Kunci Ayanamsha tidak didukung. |
| `ERR_CHART_NOT_FOUND` | 404 | ID bagan natal tidak ditemukan. |

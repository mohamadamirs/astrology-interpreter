# Spesifikasi Fitur 07: Jurnal Refleksi Empiris (Astro-Journal)

**Kode Fitur:** FEAT-07  
**Kategori:** Empirical Tracking & Event Anchoring  
**Status:** Disetujui  

---

## 1. Deskripsi & Nilai Pengguna

Fitur **Jurnal Refleksi Empiris** adalah instrumen riset personal bagi pengguna:
* Mengubah astrologi dari sekadar "percaya ramalan" menjadi metode pengujian empiris atas pola hidup sendiri.
* Pengguna mencatat peristiwa nyata di tanggal tertentu, dan sistem secara otomatis mengunci konfigurasi astronomis saat itu (*celestial snapshot*), memungkinkan pengguna memvalidasi apakah ada korelasi antara pergerakan langit dan realitas hidupnya.

---

## 2. Dekomposisi Entitas Data Jurnal (Tingkat Atomik)

### Tabel Basis Data: `journal_entries`
| Kolom | Tipe Data | Batasan (*Constraints*) | Deskripsi |
| :--- | :--- | :--- | :--- |
| `id` | `UUID` | Primary Key | Pengenal unik catatan jurnal. |
| `chart_id` | `UUID` | Foreign Key `saved_charts.id`, Indexed | Bagan natal yang menjadi jangkar referensi. |
| `event_utc` | `TIMESTAMPTZ` | Not Null, Indexed | Tanggal dan jam persis peristiwa terjadi. |
| `note_text` | `TEXT` | Not Null (Maks 5000 karakter) | Catatan deskripsi peristiwa nyata dari pengguna. |
| `subjective_tags`| `VARCHAR(50)[]`| Nullable | Tag kategori pilihan pengguna (`WORK`, `HEALTH`, `RELATIONSHIP`, `EMOTIONAL`, `FINANCE`). |
| `sky_snapshot` | `JSONB` | Not Null | Kuncian data astronomis permanen pada jam kejadian (aspek aktif, orb, Dasha). |
| `alignment_score`| `NUMERIC(3,2)` | Nullable | Skor kecocokan antara domain transit dan tag subjektif (0.00 s.d. 1.00). |
| `created_at` | `TIMESTAMPTZ` | Default `NOW()` | Stempel waktu entri dibuat. |

---

## 3. Pipa Penguncian Snapshot Langit (*Celestial Snapshot Anchoring*)

```mermaid
sequenceDiagram
    autonumber
    actor User as Pengguna
    participant UI as Jurnal Screen (UI)
    participant API as API Server (/api/v1/journal/log)
    participant Transit as TransitEngine
    participant Dasha as DashaEngine
    participant DB as Database (PostgreSQL)

    User->>UI: Ketik Catatan: "Promosi mendadak & konflik tanggung jawab tim"
    User->>UI: Pilih Tanggal: 2026-08-14 09:00 WIB & Tag: [WORK, CAREER]
    UI->>API: POST /api/v1/journal/log {chart_id, event_datetime, note_text, tags}
    activate API

    API->>Transit: calculate_transit_positions_and_aspects(chart_id, target_utc)
    activate Transit
    Note over Transit: Hitung seluruh aspek transit terhadap natal pada jam kejadian:<br/>1. Transit Saturnus Oposisi Matahari Natal (orb 0.04°)<br/>2. Transit Mars Konjungsi Midheaven (orb 0.8°)<br/>Petakan domain: Career/Situational & Mental/Cognitive
    Transit-->>API: active_transits_payload
    deactivate Transit

    API->>Dasha: get_active_dasha_hierarchy(chart_id, target_utc)
    activate Dasha
    Note over Dasha: Identifikasi level hierarki Dasha saat peristiwa:<br/>MD: Saturnus, AD: Saturnus, PD: Merkurius
    Dasha-->>API: dasha_snapshot
    deactivate Dasha

    API->>DB: INSERT INTO journal_entries (chart_id, event_utc, note_text, sky_snapshot, tags)
    activate DB
    DB-->>API: {entry_id: "uuid-9988", created_at}
    deactivate DB

    API-->>UI: HTTP 201 Created: {entry_id, anchored_transits}
    deactivate API

    UI->>UI: Pasang Kartu Jurnal pada Linimasa Transit
    UI-->>User: Tampilkan Entri Jurnal Terkunci Bersama Posisi Langit
```

---

## 4. Tampilan Linimasa & Validasi Korelasi Empiris

1. **Integrasi Linimasa Transit:**
   * Setiap tanggal yang memiliki catatan jurnal ditandai dengan ikon pena pada *Scrubber Slider* dan *Kalender*.
   * Mengetuk tanggal langsung menampilkan perbandingan berdampingan: **Peristiwa Nyata Anda** vs **Konfigurasi Langit Saat Itu**.
2. **Indeks Validasi Korelasi:**
   * Sistem menghitung seberapa sering peristiwa kategori `HEALTH` terjadi bertepatan dengan aspek stres pada penguasa Rumah ke-6 atau transit Saturnus/Mars terhadap Ascendant.

---

## 5. Struktur Kontrak JSON

### Request: `POST /api/v1/journal/log`
```json
{
  "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "event_datetime_local": "2026-08-14T16:00:00",
  "iana_timezone": "Asia/Jakarta",
  "note_text": "Menerima promosi jabatan mendadak namun terjadi perselisihan sengit mengenai delegasi tugas tim.",
  "subjective_tags": ["WORK", "CAREER", "STRESS"]
}
```

### Response Body (`HTTP 201 Created`)
```json
{
  "status": "success",
  "entry_id": "8b9e6c2d-88f1-432a-bc91-912837264819",
  "anchored_astronomy": {
    "utc_timestamp": "2026-08-14T09:00:00Z",
    "dominant_transit": "Saturn Opposition Sun (Orb 0.04°)",
    "secondary_transit": "Mars Conjunction Midheaven (Orb 0.81°)",
    "active_dasha": "Saturn - Saturn - Mercury",
    "calculated_domains": ["Career/Situational", "Mental/Cognitive"]
  }
}
```

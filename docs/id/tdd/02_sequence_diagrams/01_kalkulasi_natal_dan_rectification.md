# Sequence Diagram 01: Kalkulasi Bagan Natal & Penyesuaian Jam Lahir (Rectification Slider)

**ID Dokumen:** SD-ASTRO-001  
**Fitur Terkait:** Fitur 1 (Pengecekan Birth Chart Dual-Method), Fitur 2 (Visualisasi Bagan Ganda), Fitur 3 (Penyimpanan Chart), Fitur 4 (Rectification Slider)  
**Status:** Disetujui  

---

## 1. Deskripsi Skenario

Diagram ini memodelkan alur interaksi menyeluruh saat:
1. Pengguna memasukkan tanggal lahir, jam lahir, dan memilih lokasi presisi menggunakan pin jatuh (*pin-drop*) pada peta.
2. Sistem secara luring (*offline*) mendeteksi zona waktu IANA dan mengonversi waktu sipil lokal ke UTC kanonikal.
3. *Domain Core* mengeksekusi komputasi astronomis ganda secara paralel: Kerangka Barat (*Tropical*) dan Kerangka India (*Sidereal* Lahiri).
4. Pengguna yang memiliki keraguan menit lahir menggeser *Rectification Slider* secara interaktif di layar untuk mengamati perubahan derajat Ascendant (Lagna) dan batas rumah secara instan (*low latency*).
5. Pengguna menyimpan bagan yang telah terkonfirmasi ke dalam basis data.

---

## 2. Partisipan Sistem

* **Pengguna (User):** Aktor akhir yang berinteraksi dengan antarmuka.
* **UI_App (Expo React Native Client):** Antarmuka klien (Form Input, Peta Pin, Roda SVG, Slider).
* **API_Gateway (FastAPI Router):** Penerima request RESTful `/api/v1/chart/calculate` dan `/api/v1/chart/save`.
* **GeoTimeService:** Engine resolusi poligon spasial luring `timezonefinder` dan konversi DST `zoneinfo`.
* **EphemerisCore:** Pustaka astronomis presisi tinggi (`pyswisseph` / `ephem`) untuk koordinat geosentris.
* **AnglesHousesCore:** Algoritma komputasi GST, LST, RAMC, Midheaven, Ascendant, dan House Cusps (Placidus & Whole Sign).
* **JyotishDashaCore:** Algoritma pemetaan Nakshatra, Pada, Sub-Lord KP, dan pohon hierarki Vimshottari Dasha 4 lapis.
* **ChartRepository (Database):** Penyimpanan profil permanen PostgreSQL / SQLite via SQLAlchemy 2.0.

---

## 3. Sequence Diagram (Mermaid)

```mermaid
sequenceDiagram
    autonumber
    actor User as Pengguna
    participant UI as UI_App (React Native Expo)
    participant API as API_Gateway (FastAPI)
    participant Geo as GeoTimeService
    participant Ephem as EphemerisCore
    participant Angles as AnglesHousesCore
    participant Jyotish as JyotishDashaCore
    participant DB as ChartRepository (PostgreSQL/SQLite)

    %% Skenario 1: Ingesti Awal dan Kalkulasi Lengkap
    User->>UI: Pilih Titik Lahir pada Peta Pin (Lat, Lon) & Masukkan Jam/Tanggal
    User->>UI: Tekan Tombol "Hitung Bagan"
    UI->>API: POST /api/v1/chart/calculate {lat, lon, local_datetime, ayanamsha: "lahiri"}
    
    activate API
    API->>Geo: resolve_timezone_and_utc(lat, lon, local_datetime)
    activate Geo
    Note over Geo: Kueri poligon offline in-process (timezonefinder)<br/>Resolusi aturan DST historis via zoneinfo
    Geo-->>API: {iana_timezone: "Asia/Jakarta", utc_timestamp: "2007-08-28T23:40:00Z", julian_day: 2454341.4861}
    deactivate Geo

    par Komputasi Efemeris Geosentris & Sudut
        API->>Ephem: compute_planetary_positions(julian_day)
        activate Ephem
        Note over Ephem: Hitung posisi 10 planet + True Rahu/Ketu<br/>kecepatan harian & penanda retrograde
        Ephem-->>API: raw_ecliptic_coordinates[]
        deactivate Ephem
    and Komputasi Sudut & Rumah (Angles & Houses)
        API->>Angles: compute_ascendant_and_cusps(julian_day, lat, lon, "placidus")
        activate Angles
        Note over Angles: Hitung GST, LST, RAMC<br/>Hitung Ascendant (Lagna) & 12 House Cusps
        Angles-->>API: {ascendant_deg, mc_deg, house_cusps[1..12]}
        deactivate Angles
    end

    API->>Jyotish: compute_vedic_matrix(raw_ecliptic_coordinates, ascendant_deg, ayanamsha)
    activate Jyotish
    Note over Jyotish: Kurangkan Ayanamsha Lahiri (Apparent -> Sidereal)<br/>Hitung Nakshatra, Pada, Sub-Lord KP & Martabat<br/>Bangun pohon Vimshottari Dasha 4 Lapis (MD, AD, PD, SD)
    Jyotish-->>API: {sidereal_planets[], nakshatras[], dasha_tree}
    deactivate Jyotish

    API-->>UI: HTTP 200 OK: FullChartResponse (Western & Vedic Data)
    deactivate API

    UI->>UI: Render Dual Chart (Roda Barat 360° & Kotak Weda)
    UI-->>User: Tampilkan Dasbor Visual Bagan Ganda Lengkap

    %% Skenario 2: Penyesuaian Jam Lahir (Rectification Slider)
    opt Pengguna Menggeser Slider Penyesuaian Jam (e.g. +15 menit)
        User->>UI: Geser Slider Penyesuaian (+15 menit)
        Note over UI: UI dapat melakukan interpolasi cepat secara lokal<br/>atau memanggil endpoint lightweight recalculate_angles
        UI->>API: POST /api/v1/chart/recalculate-angles {base_utc, offset_minutes: 15, lat, lon}
        activate API
        API->>Angles: compute_ascendant_and_cusps(new_julian_day, lat, lon)
        Angles-->>API: {new_ascendant, new_cusps}
        API->>Jyotish: compute_vedic_ascendant(new_ascendant, ayanamsha)
        Jyotish-->>API: {new_lagna_sign, new_nakshatra_pada}
        API-->>UI: HTTP 200 OK: {ascendant, lagna, cusps} (Latensi < 15ms)
        deactivate API
        UI->>UI: Pembaruan Animasi Real-time pada Derajat Lagna & Garis Rumah
        UI-->>User: Tampilan Derajat Ascendant & Batas Rumah Baru
    end

    %% Skenario 3: Simpan Bagan ke Database
    User->>UI: Tekan Tombol "Simpan Profil Bagan"
    UI->>API: POST /api/v1/chart/save {profile_name, coordinates, validated_utc, chart_payload}
    activate API
    API->>DB: INSERT INTO saved_charts (user_id, name, lat, lon, utc_time, chart_data)
    DB-->>API: {chart_id: "uuid-1234", created_at: "2026-09-08T09:48:00Z"}
    API-->>UI: HTTP 201 Created: {status: "success", chart_id: "uuid-1234"}
    deactivate API
    UI-->>User: Tampilkan Konfirmasi Profil Berhasil Disimpan
```

---

## 4. Penanganan Kasus Khusus (*Edge Cases*)

| Kasus Khusus | Risiko | Mekanisme Penanganan |
| :--- | :--- | :--- |
| **Wilayah Lintang Ekstrem ($>66^\circ$)** | Sistem rumah Placidus gagal terbagi (*intercepted/broken cusps*). | Otomatis *fallback* atau beri opsi transisi ke sistem rumah *Whole Sign* atau *Porphyry* dengan pesan diagnostik yang jelas. |
| **Tanggal Lahir pada Jam Transisi DST** | Kerancuan waktu ganda (*ambiguous time*) saat jam dimundurkan. | `zoneinfo` menggunakan flag `fold=0` / `fold=1` untuk membedakan secara tegas waktu sebelum dan sesudah peralihan. |
| **Penggeseran Slider Terlalu Cepat (*High-Frequency Scrubbing*)** | Banjir request ke API (*network congestion*). | Frontend menerapkan teknik *debounce/throttle* (100 ms) saat slider bergerak, dan komputasi trigonometri Ascendant sederhana dijalankan langsung di thread klien untuk rendering instan 60 FPS. |
| **Profil Bayi yang Baru Lahir (Julian Date Real-Time)** | Delta $\Delta T$ (selisih TT dan UT) belum terpublikasi definitif. | Gunakan estimasi polinomial NASA/IERS untuk $\Delta T$ terkini dengan presisi sub-detik busur. |

---

## 5. Struktur Kontrak Data (Contoh Ringkas)

### Request: `POST /api/v1/chart/calculate`
```json
{
  "latitude": -6.175392,
  "longitude": 106.827153,
  "local_datetime": "2007-08-29T06:40:00",
  "ayanamsha": "lahiri",
  "house_system": "placidus"
}
```

### Response: `HTTP 200 OK`
```json
{
  "status": "success",
  "meta": {
    "iana_timezone": "Asia/Jakarta",
    "utc_timestamp": "2007-08-28T23:40:00Z",
    "julian_day": 2454341.486111,
    "ayanamsha_value": 23.9631
  },
  "western": {
    "ascendant": 156.421,
    "midheaven": 66.184,
    "houses": [156.421, 185.12, 214.33, 246.18, 278.45, 308.12, 336.42, 5.12, 34.33, 66.18, 98.45, 128.12],
    "planets": {
      "Sun": {"longitude": 155.12, "speed": 0.965, "is_retrograde": false, "house": 12},
      "Moon": {"longitude": 342.48, "speed": 13.12, "is_retrograde": false, "house": 7}
    }
  },
  "vedic": {
    "lagna": {"longitude": 132.458, "sign": "Leo", "nakshatra": "Purva Phalguni", "pada": 1},
    "planets": {
      "Sun": {"longitude": 131.157, "sign": "Leo", "nakshatra": "Magha", "pada": 4, "dignity": "Swakshetra"},
      "Moon": {"longitude": 318.517, "sign": "Aquarius", "nakshatra": "Shatabhisha", "pada": 4, "dignity": "Neutral"}
    },
    "vimshottari_dasha": {
      "current_mahadasha": "Saturn",
      "current_antardasha": "Saturn",
      "current_pratyantardasha": "Mercury"
    }
  }
}
```

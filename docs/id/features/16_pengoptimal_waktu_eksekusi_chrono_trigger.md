# Spesifikasi Fitur 16: Pengoptimal Waktu Eksekusi Chrono-Trigger (Precision Muhurta)

**Kode Fitur:** FEAT-16  
**Kategori:** Chrono-Trigger Optimization & Electional Mechanics  
**Status:** Disetujui  

---

## 1. Deskripsi & Nilai Pengguna

Fitur **Pengoptimal Waktu Eksekusi (*Execution Chrono-Trigger*)** menggantikan pencarian "hari baik mistis" dengan algoritma optimasi waktu berbasis kriteria objektif kuantitatif:
* Pengguna menentukan jenis aksi strategis yang akan diambil (misal: *Penandatanganan Kontrak Bisnis*, *Peluncuran Aplikasi / Go-Live*, *Investasi Modal Besar*, atau *Negosiasi Berisiko Tinggi*).
* Mesin memindai efemeris jam demi jam (*hourly step*) sepanjang rentang tanggal yang dipilih (misal 14–60 hari ke depan) untuk menghitung **Indeks Kelayakan Eksekusi (*Execution Suitability Score*)**.
* Menghasilkan peringkat jendela waktu paling optimal hingga tingkat menit beserta dekomposisi bobot matematis yang mendasarinya secara transparan.

---

## 2. Dekomposisi Input & Parameter Kriteria (Tingkat Atomik)

| Parameter | Tipe Data | Format / Satuan | Rentang Validasi | Deskripsi |
| :--- | :--- | :--- | :--- | :--- |
| `chart_id` | `UUID` | UUIDv4 | Terdaftar di DB | Profil natal pemrakarsa aksi (opsional/rekomendasi). |
| `intent_category` | `enum` | String | `CONTRACT_SIGNING`, `TECH_LAUNCH`, `LEGAL_FILING`, `FINANCIAL_INVEST` | Kategori aksi strategis. |
| `start_date` | `string` | ISO-8601 (`YYYY-MM-DD`) | Tanggal sekarang s.d. $+90$ hari | Awal rentang waktu pencarian. |
| `end_date` | `string` | ISO-8601 (`YYYY-MM-DD`) | $\le \text{start\_date} + 60\text{ hari}$ | Akhir rentang waktu pencarian. |
| `location_lat` | `float` | Derajat Desimal ($^\circ$) | $-90.000000 \le \text{lat} \le +90.000000$ | Koordinat lokasi fisik eksekusi aksi. |
| `location_lon` | `float` | Derajat Desimal ($^\circ$) | $-180.000000 \le \text{lon} \le +180.000000$| Bujur lokasi fisik eksekusi aksi. |

---

## 3. Algoritma & Matriks Pembobotan Objektif

```mermaid
flowchart TD
    Start([Pilih Kategori Aksi & Rentang Tanggal]) --> SetupWeights[Tentukan Bobot Planet Signifikator & Penalti]
    SetupWeights --> HourlyLoop[Iterasi Simulasi Waktu per Jam: t = t + 1 Jam]
    
    HourlyLoop --> CalcSky[Hitung Posisi Planet, Rumah Lokal, & Aspek pada Jam t]
    CalcSky --> CheckHardFilters{Lolos Hard Constraint? Bebas Combust / Malefic Spike?}
    
    CheckHardFilters -- Gagal --> AssignZeroScore[Beri Skor Penalti / Buang Jendela Waktu]
    CheckHardFilters -- Lolos --> SumScore[Hitung Skor Agregat S(t)]
    
    AssignZeroScore --> CheckRange{Selesai Rentang Tanggal?}
    SumScore --> CheckRange
    
    CheckRange -- Belum --> HourlyLoop
    CheckRange -- Selesai --> ClusterWindows[Klasterisasi Jam Bernilai Tinggi ke Jendela Waktu]
    ClusterWindows --> RankWindows[Urutkan Top 3 Jendela Waktu Eksekusi Terbaik]
```

### Formulasi Indeks Kelayakan Eksekusi ($S(t)$):
$$S(t) = \sum_{i=1}^M w_i \cdot C_i(t) - \sum_{j=1}^K v_j \cdot P_j(t)$$

1. **Faktor Konstruktif ($C_i$):**
   * Penguasa Rumah ke-10 atau ke-1 natal/mundane berada dalam kondisi kuat (*exalted* atau *own sign*): $+3.5$
   * Sudut harmonis (Trine/Sextile) antara Merkurius dan Jupiter (untuk kontrak/bisnis): $+4.0$
   * Bulan berada dalam fase bertumbuh (*Waxing*) dan tidak *Void of Course*: $+2.5$
2. **Faktor Penalti Friksi ($P_j$):**
   * Planet signifikator utama mengalami *Retrograde*: $-4.0$
   * Planet signifikator mengalami *Combustion* (terlalu dekat dengan Matahari, orb $< 3^\circ$): $-5.0$
   * Transit Mars atau Saturnus membentuk aspek konjungsi/oposisi/square rapat (orb $\le 1^\circ$): $-6.0$

---

## 4. Penanganan Edge Cases

1. **Tidak Ada Jendela Waktu Ideal dalam Rentang yang Dipilih:** Sistem menolak memanipulasi skor demi menyenangkan pengguna; antarmuka akan memberikan peringatan tegas: *"Seluruh jendela waktu dalam rentang ini memiliki resistensi transit tinggi. Skor tertinggi hanya 4.2/10."*
2. **Kondisi Void of Course (VOC) Bulan:** Waktu di mana Bulan tidak lagi membuat aspek mayor sebelum berganti tanda zodiak otomatis dikenakan penalti untuk inisiasi proyek baru.

---

## 5. Struktur Kontrak JSON

### Request: `POST /api/v1/chrono-trigger/optimize`
```json
{
  "chart_id": "c7a84091-28cf-4351-b8d1-580a6b7d532a",
  "intent_category": "CONTRACT_SIGNING",
  "start_date": "2026-09-15",
  "end_date": "2026-09-30",
  "latitude": -6.2088,
  "longitude": 106.8456
}
```

### Response Body (`HTTP 200 OK`)
```json
{
  "status": "success",
  "intent": "CONTRACT_SIGNING",
  "scanned_hours_total": 360,
  "recommended_windows": [
    {
      "rank": 1,
      "score": 9.2,
      "start_local": "2026-09-22T10:15:00+07:00",
      "end_local": "2026-09-22T12:45:00+07:00",
      "primary_benefic_drivers": [
        "Mercury in Virgo (Exalted & Direct motion) in 10th house",
        "Moon Trine Jupiter (Orb 0.28°)",
        "Waxing Moon phase without Void of Course"
      ],
      "risk_factors_avoided": [
        "Zero combustion on Mercury",
        "Mars and Saturn are cadent with no hard aspects to ascendant"
      ]
    }
  ]
}
```

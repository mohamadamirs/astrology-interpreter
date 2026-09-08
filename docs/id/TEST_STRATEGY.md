# Jaminan Kualitas & Strategi Pengujian

## 1. Prinsip Utama
* **Determinisme Matematis:** Input yang sama wajib menghasilkan output yang identik secara biner.
* **Toleransi Benchmark Efemeris:** Posisi planet wajib cocok dengan vektor acuan Swiss Ephemeris / NASA JPL dalam batas $\pm 0.001^\circ$ ($3.6$ detik busur).
* **Zero Network I/O Saat Test:** Pencarian zona waktu wajib murni mengandalkan berkas poligon lokal.

---

## 2. Vektor Acuan Kebenaran Darat (*Ground Truth*)

### Vektor 1: Acuan Standar Khatulistiwa
* **Input:** `2007-08-29 06:40:00 WIB` (`2007-08-28 23:40:00 UTC`), Lat `-6.8700`, Lon `109.0400` (Brebes).
* **Hasil Wajib:**
  * Ascendant (Lagna): Sidereal Leo $25^\circ 32' \pm 0.05^\circ$ (*Purva Phalguni 4*).
  * Bulan (Chandra): Sidereal Aquarius $18^\circ 31' \pm 0.02^\circ$ (*Shatabhisha 4*).
  * Matahari (Surya): Sidereal Leo $11^\circ 13' \pm 0.01^\circ$ (*Magha 4*).
  * Dasha saat 2026-09-08: Mahadasha **Saturnus**, Antardasha **Saturnus** (*Swabhukti*).

### Vektor 2: Konjungsi Eksak (Gerhana Matahari Total)
* **Input:** `1999-08-11 11:03:00 UTC`, Lat `48.1351`, Lon `11.5820` (Munich).
* **Hasil Wajib:**
  * Bujur tropikal Matahari dan Bulan cocok dalam selisih $\Delta \le 0.001^\circ$.
  * Engine aspek melaporkan Konjungsi dengan orb $\le 0.002^\circ$.

### Vektor 3: Titik Rumah Lintang Kutub (*Fallback Placidus*)
* **Input:** `2024-12-21 12:00:00 UTC`, Lat `69.6492`, Lon `18.9553` (Tromsø, Norwegia).
* **Hasil Wajib:**
  * Sistem mendeteksi kegagalan kuadran lingkaran kutub dan secara mulus beralih ke Whole Sign tanpa galat *division-by-zero*.

---

## 3. Matriks Pengujian & Alat

| Lapisan | Alat | Target Metrik |
| :--- | :--- | :--- |
| **Unit Engine** | `pytest`, `pytest-cov` | Cakupan $\ge 90\%$; delta benchmark $\le 0.001^\circ$. |
| **Integrasi API** | `httpx.AsyncClient` | 100% validasi skema, status kode, payload error. |
| **UI Klien** | `jest`, React Native Testing Library | Pemicu event peta, render SVG bagan. |

# Dokumen Kebutuhan Produk (PRD)

## 1. Visi Produk
Engine astrologi lintas platform (Mobile & Web) berpresisi tinggi yang mengeliminasi dua kelemahan industri:
1. **Ketidakakuratan Koordinat Kota:** Mengganti pencarian nama kota umum dengan pembacaan GPS fisik dan penempatan pin di peta (*map pin-drop*).
2. **Sikofansi Interpretasi (*Barnum Effect*):** Mengganti pujian manis/ramalan manipulatif dengan mesin pembobotan 5-domain deterministik yang memetakan friksi dan alur konstruktif secara objektif.

---

## 2. Cakupan Sistem

### 2.1 Masuk Cakupan (MVP)
* Pemilihan koordinat via pin peta ($\pm 11\text{m}$ presisi) dan deteksi GPS perangkat otomatis.
* Resolusi zona waktu IANA offline dan normalisasi offset UTC historis (termasuk DST).
* Perhitungan Zodiak Ganda: Tropikal (Sayana) dan Sidereal (Lahiri default, KP, Raman, Fagan-Bradley).
* Pembagian divisi Weda: 27 Nakshatra, 108 Pada, Sub-Lord KP, D1 (Rashi), D9 (Navamsha).
* Engine Vimshottari Dasha 4 tingkat hierarkis (MD, AD, PD, SD).
* Engine aspek geometri transit dengan pembobotan peluruhan eksponensial kontinu ($W = 10 \cdot e^{-1.4 \cdot \text{orb}}$).
* Skor dampak 5-Domain: Mental, Emosional, Karier, Interpersonal, Vitalitas.
* Klien universal (iOS, Android, Web via Expo) yang merender bagan SVG interaktif (Vedic Selatan/Utara & Roda Barat).

### 2.2 Luar Cakupan (Pasca-MVP)
* Komparasi bagan multi-pengguna (*synastry/composite*).
* Matriks numerik lengkap Ashtakavarga.
* Integrasi payment gateway dan manajemen langganan.

---

## 3. Kebutuhan Fungsional

### 3.1 Ingesti Geospasial & Waktu (`GEO-TIME`)
* **FR-GEO-01:** Klien harus menangkap koordinat GPS hardware melalui `expo-location`.
* **FR-GEO-02:** Klien harus menyediakan peta interaktif dengan pin yang dapat digeser, menghasilkan lintang/bujur WGS84 hingga 4 desimal.
* **FR-GEO-03:** Backend harus memetakan koordinat ke zona waktu IANA resmi (misal `Asia/Jakarta`) 100% offline via poligon lokal (`timezonefinder`).
* **FR-GEO-04:** Backend harus menghitung timestamp UTC kanonikal menggunakan Python `zoneinfo`, memperhitungkan aturan DST historis pada tanggal lahir tersebut.

### 3.2 Efemeris & Posisi Astronomis (`ASTRO-CORE`)
* **FR-AST-01:** Menghitung bujur, lintang ekliptika geosentris, dan kecepatan harian untuk Matahari, Bulan, Merkurius, Venus, Mars, Jupiter, Saturnus, Uranus, Neptunus, Pluto.
* **FR-AST-02:** Menghitung Simpul Bulan (*True* dan *Mean Node*). Ketu harus selalu $180^\circ$ berlawanan dengan Rahu.
* **FR-AST-03:** Menandai status retrograde (`is_retrograde = True`) jika dan hanya jika kecepatan harian bujur $< 0$ (kecuali Matahari dan Bulan).
* **FR-AST-04:** Menurunkan RAMC, Ascendant (Lagna), dan Midheaven (MC) dari Waktu Sideris Lokal. Mendukung sistem rumah Whole Sign, Placidus, dan Equal.
* **FR-AST-05:** Mengonversi posisi tropikal ke sidereal via pengurangan Ayanamsha presesi IAU: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropikal}} - \text{Ayanamsha}) \pmod{360^\circ}$.

### 3.3 Divisi Weda & Engine Dasha (`JYOTISH-CORE`)
* **FR-JYO-01:** Membagi bujur sidereal ke dalam 27 Nakshatra ($13^\circ 20'$ per nakshatra) dan 4 Pada ($3^\circ 20'$ per pada).
* **FR-JYO-02:** Menurunkan Sub-Lord KP menggunakan busur proporsional Vimshottari: $\text{Busur} = (800' \times \text{Tahun}) / 120$.
* **FR-JYO-03:** Menghitung penempatan zodiak D1 (Rashi) dan D9 (Navamsha) serta martabat planet (Exalted, Moolatrikona, Swakshetra, Netral, Debilitated).
* **FR-JYO-04:** Menghitung hierarki Vimshottari Dasha 4 lapis (MD, AD, PD, SD) dan matriks relasi alami (*Nisargika Sambandha*) antara penguasa MD dan AD aktif.

### 3.4 Engine Transit & Skor 5-Domain (`INTERPRET-CORE`)
* **FR-INT-01:** Mendeteksi separasi sudut untuk Konjungsi ($0^\circ$), Sekstil ($60^\circ$), Square ($90^\circ$), Trine ($120^\circ$), Oposisi ($180^\circ$), Semisquare ($45^\circ$), Sesquiquadrate ($135^\circ$), Quincunx ($150^\circ$).
* **FR-INT-02:** Menghitung bobot aspek via peluruhan eksponensial: $W = 10.0 \times e^{-1.4 \times \text{orb}}$. Terapkan pengali $1.5\times$ jika aspek menyentuh penguasa MD atau AD aktif.
* **FR-INT-03:** Memetakan aspek transit dan baseline Dasha ke dalam delta skor integer pada 5 domain:
  * `mental_cognitive` (Fokus, kapasitas analitis vs overthinking)
  * `emotional_psychological` (Ketenangan batin vs friksi/frustrasi)
  * `career_situational` (Daya dorong eksekusi vs hambatan struktural)
  * `interpersonal_relational` (Batasan relasi vs proyeksi stres)
  * `physiological_vitality` (Tegangan somatik, indikator Pitta/Vata)
* **FR-INT-04:** Menegakkan kategori skor ketat:
  * $\le -40$: `SEVERE FRICTION / HIGH VOLATILITY`
  * $-39 \text{ s.d. } -10$: `MODERATE PRESSURE / IRRITATION`
  * $-9 \text{ s.d. } +9$: `NEUTRAL / MIXED TENSION`
  * $\ge +10$: `CONSTRUCTIVE FLOW`

### 3.5 Antarmuka Klien Universal (`CLIENT-UI`)
* **FR-UI-01:** Satu basis kode React Native menargetkan iOS, Android, dan browser Web.
* **FR-UI-02:** Merender bagan vektor tajam (SVG) untuk format Weda India Selatan, India Utara, dan Roda Sirkular Barat 360°.
* **FR-UI-03:** Menampilkan kartu barometer 5-domain berkode warna dan vonis strategis objektif (*unvarnished verdict*).

---

## 4. Kebutuhan Non-Fungsional (NFR)
* **NFR-PERF-01 (Latensi):** Kalkulasi chart natal + Dasha + pemetaan transit $\le 150\text{ ms}$.
* **NFR-PERF-02 (Lookup Offline):** Resolusi koordinat ke zona waktu $\le 10\text{ ms}$ tanpa kueri jaringan.
* **NFR-ACC-01 (Presisi):** Bujur planet cocok dengan vektor benchmark Swiss Ephemeris / NASA JPL dalam toleransi $\pm 0.001^\circ$ ($3.6$ detik busur).
* **NFR-DET-01 (Determinisme):** Input yang sama wajib menghasilkan respons JSON yang identik hingga tingkat bit.
* **NFR-PRIV-01 (Privasi):** Koordinat geografis tidak boleh dikirim ke analitik pihak ketiga.

# GEMINI.md - Context & Project Memory

> **Status:** Draft / Temporary Context File (Living Document - Akan terus diperbarui seiring evolusi proyek).  
> **Tujuan File:** Memberikan panduan konteks menyeluruh bagi AI assistant (Gemini/Claude/GPT) dan pengembang mengenai visi, arsitektur, batasan teknis, serta peta navigasi dokumen proyek ini.

---

## 1. Identitas & Esensi Proyek

**Astrology-Interpreter** adalah platform komputasi astrologi lintas platform (**Mobile iOS/Android & Web**) dengan dua pilar utama yang membedakannya dari aplikasi komersial umum:
1. **Presisi Koordinat Fisik (Bukan Centroid Kota):** Menggunakan koordinat fisik (GPS / Pin Peta) yang dipetakan secara **100% offline** ke zona waktu IANA dan offset UTC historis (termasuk DST).
2. **Determinisme & Anti-Sikofansi (Tanpa Ramalan Manis):** Menerapkan fungsi matematika peluruhan eksponensial dan matriks keputusan 5-Domain (*Mental, Emosional, Karier, Relasi, Vitalitas*) untuk memetakan friksi dan alur konstruktif secara objektif tanpa bias pujian palsu (*Barnum/Forer Effect*).

---

## 2. Ringkasan Tech Stack & Arsitektur

* **Backend Engine:** Python 3.11+ | FastAPI | PyEphem / Swiss Ephemeris (`ephem`) | `timezonefinder` + `zoneinfo`
* **Frontend Universal:** React Native (Expo SDK 51+) | `react-native-web` | `react-native-svg` | `expo-location`
* **Database & ORM:** PostgreSQL 16+ (Produksi) / SQLite 3 (Lokal) | SQLAlchemy 2.0 | Alembic
* **State & Query:** Zustand | TanStack Query v5 | Axios

---

## 3. Peta Navigasi Dokumentasi Lengkap (*Documentation Map*)

Seluruh spesifikasi teknis matang telah disusun dalam format dwibahasa di folder [`docs/`](./docs):

### 🇮🇩 Bahasa Indonesia (`docs/id/`)
* 📄 **[`docs/id/PRD.md`](./docs/id/PRD.md)** — Kebutuhan produk, cakupan MVP, spesifikasi modul (GEO-TIME, ASTRO-CORE, JYOTISH, INTERPRET, CLIENT-UI).
* 🏗️ **[`docs/id/ARCHITECTURE.md`](./docs/id/ARCHITECTURE.md)** — Desain sistem teknis, struktur folder backend/frontend, dan formula matematika.
* 🔌 **[`docs/id/API_SPEC.md`](./docs/id/API_SPEC.md)** — Spesifikasi kontrak REST API, format envelope, dan katalog kode error.
* 🗄️ **[`docs/id/DATA_SCHEMA.md`](./docs/id/DATA_SCHEMA.md)** — ERD database, definisi tabel SQLAlchemy/PostgreSQL, dan indeks performa.
* 🧪 **[`docs/id/TEST_STRATEGY.md`](./docs/id/TEST_STRATEGY.md)** — Strategi QA, vektor acuan ground-truth benchmark, dan ambang batas toleransi.
* 🗺️ **[`docs/id/ROADMAP.md`](./docs/id/ROADMAP.md)** — Rencana rilis 5 sprint, backlog task per-file, dan kriteria Definition of Done (DoD).
* 🏛️ **[`docs/id/adr/`](./docs/id/adr/README.md)** — 6 Rekaman Keputusan Arsitektur (Python FastAPI, Expo, Offline TZ, Dual-Zodiac, Exponential Orb, Hourly Cache).

### 🇬🇧 English (`docs/en/`)
* 📄 **[`docs/en/PRD.md`](./docs/en/PRD.md)** — Product Requirements Document (Scope, Modules, Anti-sycophancy rules).
* 🏗️ **[`docs/en/ARCHITECTURE.md`](./docs/en/ARCHITECTURE.md)** — Technical Design Document (Pipelines, Directory layout).
* 🔌 **[`docs/en/API_SPEC.md`](./docs/en/API_SPEC.md)** — REST API Contracts & Error Catalog.
* 🗄️ **[`docs/en/DATA_SCHEMA.md`](./docs/en/DATA_SCHEMA.md)** — Database Schema & Data Models.
* 🧪 **[`docs/en/TEST_STRATEGY.md`](./docs/en/TEST_STRATEGY.md)** — QA & Ephemeris Benchmark Testing Strategy.
* 🗺️ **[`docs/en/ROADMAP.md`](./docs/en/ROADMAP.md)** — 5-Sprint Backlog & Definition of Done.
* 🏛️ **[`docs/en/adr/`](./docs/en/adr/README.md)** — Architecture Decision Records (ADR-0001 through ADR-0006).

---

## 4. Batasan Teknis & Panduan Pengembang / AI (*Guardrails*)

Saat menulis atau memodifikasi kode di repositori ini, patuhi aturan berikut:
1. **Dilarang Menambah Kueri Jaringan untuk Lokasi di Backend:** Resolusi zona waktu wajib menggunakan poligon lokal `timezonefinder`, bukan API pihak ketiga berbayar/berjaringan.
2. **Kunci Sidereal pada Dasha:** Perhitungan Vimshottari Dasha dan Nakshatra hanya boleh menggunakan bujur Sidereal (Lahiri/Nirayana). Jangan pernah memasukkan bujur Tropikal ke fungsi Dasha.
3. **Fungsi Pembobotan Eksponensial Kontinu:** Jangan gunakan tabel batas orb kaku (*step-cutoff*). Gunakan selalu rumus:
   $$W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$$
4. **Prinsip Anti-Sikofansi:** Jangan pernah menyaring atau menghaluskan skor negatif dalam skrip interpretasi demi menyenangkan pengguna.
5. **Universal Client Parity:** Hindari dependensi yang hanya jalan di mobile tanpa fallback web.

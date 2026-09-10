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

* 🌐 **[Portal Dokumentasi Terpadu (`docs/README.md`)](./docs/README.md)**

### 🇮🇩 Bahasa Indonesia (`docs/id/`)
* 📄 **[`docs/id/PRD.md`](./docs/id/PRD.md)** — Kebutuhan produk, batasan non-fungsional, persona, cakupan 11 fitur inti, dan rencana rilis.
* 📂 **[`docs/id/features/INDEX.md`](./docs/id/features/INDEX.md)** — Indeks Spesifikasi 11 Fitur Atomik (FEAT-01 s.d. FEAT-11: input terperinci, formula matematika, alur algoritma, diagram Mermaid, edge cases, dan kontrak respons JSON).

### 🇬🇧 English (`docs/en/`)
* 📄 **[`docs/en/PRD.md`](./docs/en/PRD.md)** — Product Requirements Document (Scope, Non-functional requirements, and release phases).
* 📂 **[`docs/en/features/INDEX.md`](./docs/en/features/INDEX.md)** — Detailed atomic specifications for all 11 core features (FEAT-01 through FEAT-11).

---

## 4. Batasan Teknis & Panduan Pengembang / AI (*Guardrails*)

1. **Dilarang Menambah Kueri Jaringan untuk Lokasi di Backend:** Resolusi zona waktu wajib menggunakan poligon lokal `timezonefinder`.
2. **Kunci Sidereal pada Dasha:** Perhitungan Vimshottari Dasha dan Nakshatra hanya boleh menggunakan bujur Sidereal (Lahiri/Nirayana).
3. **Fungsi Pembobotan Eksponensial Kontinu:** Gunakan rumus $W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$.
4. **Prinsip Anti-Sikofansi:** Jangan pernah menyaring skor negatif demi menyenangkan pengguna.

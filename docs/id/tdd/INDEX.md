# Dokumen Desain Teknis (Technical Design Document - TDD)

Selamat datang di direktori dokumentasi teknis sistem **Astrology-Interpreter Engine & Universal Platform**. Dokumen ini disusun secara modular dan terpisah sesuai standar rekayasa perangkat lunak modern:

---

## Struktur Folder TDD

```text
docs/id/tdd/
├── 01_arsitektur_sistem.md                       # Bagian 1: Topologi, Komponen, Clean Architecture, Monorepo
├── 02_sequence_diagrams/                         # Bagian 2: Sequence Diagrams (1 Berkas per Skenario)
│   ├── INDEX.md
│   ├── 01_kalkulasi_natal_dan_rectification.md   # SD-01: Ingesti & Slider Penyesuaian Jam Lahir
│   ├── 02_transit_dan_aspect_hit_scanner.md      # SD-02: Navigasi Waktu & Aspect Hit Scanner
│   ├── 03_smart_transit_alerts.md               # SD-03: Evaluasi & Push Alerts Transit Kritis
│   ├── 04_kecocokan_multi_arketipe.md            # SD-04: Synastry Pasangan/Teman/Kerja & Orang Asing
│   ├── 05_chatbot_rag_doktrin.md                 # SD-05: AI Chatbot RAG Bebas Halusinasi
│   └── 06_jurnal_empiris_dan_berbagi.md          # SD-06: Jurnal Catatan Peristiwa & Ekspor Bagan
├── 03_adr/                                       # Bagian 3: Architecture Decision Records
│   ├── INDEX.md
│   ├── 0001-gunakan-python-fastapi.md
│   ├── 0002-adopsi-universal-expo-react-native.md
│   ├── 0003-resolusi-zona-waktu-offline.md
│   ├── 0004-arsitektur-transformasi-zodiak-ganda.md
│   ├── 0005-pembobotan-orb-peluruhan-eksponensial.md
│   ├── 0006-strategi-caching-transit-per-jam.md
│   ├── 0007-arsitektur-rag-dan-vektor-doktrin-klasik.md
│   └── 0008-kontrol-privasi-dan-ghost-mode.md
├── 04_penanganan_kegagalan.md                    # Bagian 4: Toleransi Kesalahan, Fallback & Self-Healing
└── 05_skalabilitas.md                            # Bagian 5: 3-Tier Caching, Partisi DB, HPA & Concurrency
```

---

## Ringkasan Navigasi Cepat

1. **[01. Arsitektur Sistem](file:///root/astrology-interpreter/docs/id/tdd/01_arsitektur_sistem.md):** Prinsip determinisme, pemisahan dual-core ekliptika, topologi 4-layer, dekomposisi 9 domain engine, dan layout struktur direktori monorepo.
2. **[02. Sequence Diagrams](file:///root/astrology-interpreter/docs/id/tdd/02_sequence_diagrams/INDEX.md):** 6 alur diagram sekuens interaksi mendalam, pemodelan partisipan, penanganan *edge cases*, dan kontrak data JSON.
3. **[03. Architecture Decision Records (ADR)](file:///root/astrology-interpreter/docs/id/tdd/03_adr/INDEX.md):** 8 keputusan arsitektur kunci yang melandasi pemilihan teknologi dan algoritma matematika.
4. **[04. Penanganan Kegagalan](file:///root/astrology-interpreter/docs/id/tdd/04_penanganan_kegagalan.md):** Taksonomi mitigasi kegagalan, singularitas kutub, ambiguitas DST, fail-safe bypass, dan pemulihan bencana.
5. **[05. Skalabilitas & Kinerja](file:///root/astrology-interpreter/docs/id/tdd/05_skalabilitas.md):** Profil beban kerja, 3-tier caching (In-process LRU, Redis Hourly, TanStack Query), skalabilitas horizontal stateless pod, dan partisi tabel rentang waktu.

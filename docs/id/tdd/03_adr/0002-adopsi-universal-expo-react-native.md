# ADR-0002: Adopsi Universal React Native (Expo) untuk Klien Mobile & Web

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Aplikasi ditargetkan rilis sekaligus di Android, iOS, dan Browser Web. Memelihara dua basis kode terpisah akan melipatgandakan beban kerja dan memicu inkonsistensi fitur.

## Keputusan
Memilih **Universal React Native via Expo (`react-native-web`)** karena:
1. **Berbagi Kode Tinggi:** $\ge 85\%$ logika bisnis, state management (Zustand), dan komponen UI dipakai bersama.
2. **Grafik Vektor Lintas Platform:** Library `react-native-svg` merender bagan astrologi (kotak Weda dan roda Barat) secara deterministik di kanvas mobile native maupun DOM web SVG.
3. **Navigasi Terpadu:** Expo Router mendukung deep-linking di HP dan struktur URL web standar.

## Konsekuensi
* **Positif:** Satu commit langsung memperbarui fitur di Android, iOS, dan Web secara bersamaan.
* **Trade-off:** Tampilan web bersifat SPA (client-rendered), memerlukan konfigurasi prerender bila SEO statis diutamakan pasca-MVP.

# ADR-0003: Resolusi Zona Waktu Geospasial Offline via TimeZoneFinder & ZoneInfo

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Menghitung bagan astrologi mewajibkan konversi waktu sipil lokal ke UTC. Mengandalkan API web eksternal (misal Google Timezone API) menyebabkan latensi jaringan (150-500 ms), biaya per kuota, dan risiko kebocoran privasi koordinat pengguna.

## Keputusan
Memilih **Resolusi Offline In-Memory via `timezonefinder` dan Python `zoneinfo`**:
1. **Zero Network I/O:** Pencarian batas poligon geospasial berjalan lokal di memori $\le 10\text{ ms}$.
2. **Akurasi Historis:** Basis data IANA tzdata bawaan Python menangani peralihan Daylight Saving Time (DST) historis dengan tepat.
3. **Privasi Penuh:** Koordinat fisik tidak pernah keluar dari server aplikasi.

## Konsekuensi
* **Positif:** Bebas biaya API eksternal, latensi instan, dan privasi terjamin.
* **Trade-off:** Ukuran image container bertambah $\sim 45\text{ MB}$ untuk menyimpan dataset poligon dunia.

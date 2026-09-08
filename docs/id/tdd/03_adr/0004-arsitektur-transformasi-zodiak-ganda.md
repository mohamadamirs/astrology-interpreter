# ADR-0004: Arsitektur Transformasi Zodiak Ganda (Sidereal Default + Opsi Tropikal)

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Praktisi astrologi global terbagi menjadi Barat (Tropikal/Sayana) dan Timur/Weda (Sidereal/Nirayana). Membatasi sistem hanya pada satu paradigma mempersempit adopsi pengguna.

## Keputusan
Memilih **Arsitektur Normalisasi Bujur Ekliptika dengan Lapisan Transformasi Eksplisit**:
1. Efemeris menghitung bujur ekliptika geosentris absolut $[0^\circ, 360^\circ)$ sebagai acuan dasar tunggal.
2. Posisi tropikal adalah bujur ekliptika langsung, sedangkan posisi sidereal diturunkan dari pengurangan eksplisit Ayanamsha: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropikal}} - \text{Ayanamsha}) \pmod{360^\circ}$.
3. Siklus Dasha dan Nakshatra dikunci secara ketat hanya pada data Sidereal untuk menjaga validitas matematis klasik.

## Konsekuensi
* **Positif:** Klien dapat beralih tampilan zodiak tanpa perlu kueri ulang ke mesin efemeris.
* **Trade-off:** Ukuran payload JSON bertambah $\sim 30\%$ karena membawa data kedua representasi.

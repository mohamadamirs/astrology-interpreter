# ADR-0006: Strategi Caching Posisi Transit per Jam

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Menghitung ulang posisi 10 planet dan semua kombinasi sudut aspek pada setiap request dashboard pengguna membebani CPU secara berlebihan saat trafik tinggi.

## Keputusan
Menerapkan **Hourly Discrete Bucketing dengan Cache Memori & Database**:
1. Pergeseran planet luar $< 0.01^\circ$/jam dan planet dalam $\approx 0.04^\circ$/jam, sehingga jendela 1 jam sepenuhnya aman untuk evaluasi barometer harian.
2. Truncate timestamp ke jam UTC (`YYYY-MM-DD-HH:00:00Z`) menghasilkan primary key pencarian yang deterministik.
3. Mengambil posisi transit dari cache memori memangkas latensi dari $120\text{ ms}$ menjadi $< 15\text{ ms}$.

## Konsekuensi
* **Positif:** Mengurangi beban CPU hingga $95\%$ pada jam sibuk.
* **Trade-off:** Disediakan parameter opsional `?exact=true` khusus bagi pengguna yang membutuhkan pergeseran menit presisi pada Bulan.

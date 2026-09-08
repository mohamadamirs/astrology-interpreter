# ADR-0008: Kontrol Privasi, Masking Data Kelahiran, dan Ghost Mode

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Tanggal dan jam lahir yang presisi serta koordinat GPS adalah data pribadi sensitif. Fitur sosial seperti pelacakan kecocokan dengan orang di sekitar (*Nearby*) dan orang tidak dikenal (*Stranger Profiles*) berpotensi mengekspos lokasi fisik atau privasi kelahiran pengguna. Di sisi lain, pengguna meminta agar untuk profil orang asing, seluruh dimensi kecocokan tetap dihitung dan disajikan secara utuh tanpa pengurangan.

Pilihan yang dievaluasi:
1. **Reduksi Dimensi (Truncated Synastry):** Menyembunyikan dimensi rumah atau aspek tertentu untuk profil asing. Ditolak oleh mandat pengguna.
2. **Kalkulasi Sisi Klien Penuh:** Berisiko membocorkan koordinat mentah via inspeksi paket jaringan.
3. **Pemisahan Lapisan Komputasi & Presentasi dengan Enkripsi/Masking (Ghost Mode):** Semua kalkulasi astronomis lengkap dijalankan di backend terisolasi, namun sebelum dikembalikan ke klien publik, tanggal, jam lahir, dan koordinat fisik di-masking atau diberi jitter spasial.

## Keputusan
Memilih **Pemisahan Komputasi & Presentasi dengan Masking**:
1. *Ghost Mode Active:* Menghapus penyiaran suar lokasi (*beacon*) pengguna dari daftar pencarian *Nearby*.
2. *Data Sanitization:* API menyaring parameter sensitif (`birth_time`, `exact_lat_lon`) dari payload JSON publik dan menggantinya dengan penanda anonim, tetapi mengembalikan 100% skor dimensi kecocokan yang telah dihitung lengkap.
3. *Spatial Jitter:* Untuk tampilan peta umum, koordinat ditambahkan acakan radius minimal 500 meter (*geohash fuzzing*).

## Konsekuensi
* **Positif:** Privasi pengguna terjamin aman tanpa mengurangi kedalaman analisis kecocokan.
* **Trade-off:** Memerlukan middleware pembersih data (*sanitization middleware*) yang ketat sebelum payload dikirimkan ke frontend.

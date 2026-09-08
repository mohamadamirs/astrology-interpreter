# Dokumen Kebutuhan Produk (PRD) - Inventaris Fitur Lengkap

Dokumen ini memuat **seluruh poin kebutuhan dan fitur yang diminta oleh pengguna**. Berfungsi sebagai master feature inventory sebelum dilakukan pemilahan mana yang masuk ke fase pondasi awal (MVP) dan mana yang masuk fase lanjutan.

---

## 1. Prinsip Mutlak Sistem (*Core Mandates*)

1. **Zero Tolerance pada Barnum Effect (Forer Effect):**
   * Menolak keras segala bentuk ramalan generik, kata-kata manis (*flattery*), atau kalimat abu-abu yang bisa cocok untuk semua orang.
   * Interpretasi harus objektif dan memiliki alasan kausalitas matematis posisi langit yang nyata.
2. **Presisi Tinggi dalam Interpretasi Efek Transit:**
   * Menggunakan metode yang sangat presisi dalam mengukur dampak posisi transit terhadap bagan kelahiran (*birth chart*).

---

## 2. Inventaris Fitur Lengkap

### Fitur 1: Pengecekan Birth Chart Lengkap (2 Metode)
* Pengecekan bagan kelahiran secara menyeluruh menggunakan **2 tradisi utama**:
  1. **Astrologi Barat (*Western / Tropical*)**
  2. **Astrologi India (*Vedic / Sidereal*)**

### Fitur 2: Visualisasi Bagan Zodiak Ganda (*Dual Visual Chart Rendering*)
* **Format Barat:** Roda melingkar 360 derajat (*Western Circular Wheel*) lengkap dengan garis-garis koneksi aspek geometris di tengahnya.
* **Format India:** Bagan kotak tradisional Weda (*South Indian grid* dan/atau *North Indian diamond*).
* Tabel data mentah posisi planet (derajat, menit, detik, status retrograde, dan kecepatan harian).

### Fitur 3: Penyimpanan Birth Chart (*Storage*)
* Seluruh data *birth chart* yang telah dibuat tersimpan secara permanen di penyimpanan (*storage / database*), sehingga tidak hilang dan dapat dikelola atau dibuka kembali kapan saja.

### Fitur 4: Alat Bantu Penyesuaian Jam Lahir (*Birth Time Adjuster / Slider*)
* Slider penggeser menit/jam dinamis langsung di tampilan chart untuk membantu pengguna yang jam lahirnya kurang pasti.
* Pengguna dapat menggeser waktu mundur/maju (misal $\pm 30$ menit) dan melihat langsung pergeseran derajat Ascendant (Lagna) dan batas rumah secara *real-time*.

### Fitur 5: Mesin Transit Bolak-Balik Waktu (*Time-Traveling Transit Engine*)
* Kemampuan membaca transit secara dinamis:
  * **Hari ini (*Real-time*)**
  * **Masa lalu (*Past events*)**
  * **Masa depan (*Predictive*)**
  * Bisa ditelusuri bolak-balik secara fleksibel.
* **Mode Interaksi Transit:**
  * **Slider:** Navigasi penggeser waktu maju-mundur secara dinamis.
  * **Kalender:** Tampilan kalender dengan penanda tanggal-tanggal transit penting.
  * **Pencari Momen Penting (*Aspect Hit Scanner*):** Fitur pencari otomatis untuk melompat langsung ke tanggal terjadinya transit-transit penting (misal Saturn Return, nodal return, aspek eksak).

### Fitur 6: Notifikasi Transit Kritis (*Smart Transit Alerts*)
* Peringatan otomatis (push notification) ketika terjadi transit eksak ber-orb ketat yang menghantam titik sensitif natal pengguna.
* Notifikasi murni menyajikan data astronomis objektif dan ranah yang dipengaruhi, tanpa bumbu ramalan sensasional.

### Fitur 7: Jurnal Refleksi Empiris (*Astro-Journal / Event Diary*)
* Fitur catatan harian terintegrasi dengan garis waktu transit.
* Pengguna dapat mencatat peristiwa nyata di tanggal tertentu untuk menguji dan memvalidasi korelasi empiris antara pergerakan planet dengan pengalaman hidup nyata.

### Fitur 8: Fitur Bagikan (*Share Feature*)
* Pengguna dapat membagikan bagan (*chart*) dan hasil analisisnya ke pengguna lain atau mengekspornya ke platform luar.

### Fitur 9: Kecocokan Multi-Relasi (*Compatibility / Synastry*)
* Penilaian kecocokan tidak terbatas pada hubungan pasangan romantis saja, melainkan mencakup:
  * **Pasangan** (*Romantic / Partner*)
  * **Teman** (*Friendship*)
  * **Rekan Kerja / Bisnis** (*Professional / Coworker*)
* **Sumber Profil yang Dicocokkan:**
  * Berdasarkan **Kontak HP**.
  * Berdasarkan **Orang di Sekitar (*Nearby / Proximity*)**.
  * Berdasarkan **Orang Tidak Dikenal:** Seluruh analisis dan dimensi kecocokan tetap dihitung dan ditampilkan secara lengkap dan menyeluruh.

### Fitur 10: Kontrol Privasi & Mode Penyamaran (*Privacy & Ghost Mode*)
* Sakelar privasi (*Privacy Toggle*) untuk melindungi data sensitif tanggal & jam lahir:
  * Opsi mengaktifkan/menonaktifkan deteksi *"Orang di Sekitar (*Nearby*)"*.
  * Opsi menampilkan skor kecocokan kepada orang lain tanpa membocorkan rincian data kelahiran asli pengguna.

### Fitur 11: Chatbot AI dengan Fitur RAG (*Retrieval-Augmented Generation*)
* Mengubah data astronomis mentah (*raw data*) menjadi penjelasan yang manusiawi dan komunikatif.
* Menggunakan basis rujukan dokumen otoritatif (RAG) agar jawaban AI berakar kuat pada literatur klasik yang valid, bebas halusinasi, dan menolak pola ramalan generik (*Barnum effect*).

---

## 3. Catatan Pemilihan Fase

Seluruh 11 poin di atas adalah **inventaris fitur lengkap pengguna**. Pada tahap perencanaan eksekusi berikutnya, daftar ini akan dipilah bersama pengguna untuk menetapkan:
* **Fase 1 (Fondasi Awal / MVP):** Fitur inti mutlak yang dibangun pertama kali.
* **Fase Lanjutan:** Fitur-fitur yang dikembangkan secara bertahap setelah fondasi stabil.

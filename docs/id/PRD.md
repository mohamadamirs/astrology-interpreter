# Dokumen Kebutuhan Produk (PRD) - Inventaris Fitur

Dokumen ini memuat **seluruh poin kebutuhan dan fitur yang diminta secara khusus oleh pengguna**. Dokumen ini berfungsi sebagai daftar inventaris fitur utama (*master feature inventory*) sebelum dilakukan pemilahan mana yang masuk ke tahap awal (MVP) dan mana yang dikerjakan nanti.

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

### Fitur 2: Penyimpanan Birth Chart (*Storage*)
* Seluruh data *birth chart* yang telah dibuat tersimpan secara permanen di penyimpanan (*storage / database*), sehingga tidak hilang dan dapat dibuka kembali kapan saja.

### Fitur 3: Mesin Transit Bolak-Balik Waktu (*Time-Traveling Transit Engine*)
* Kemampuan membaca transit secara dinamis:
  * **Hari ini (*Real-time*)**
  * **Masa lalu (*Past events*)**
  * **Masa depan (*Predictive*)**
  * Bisa ditelusuri bolak-balik secara fleksibel.
* **Mode Interaksi Transit:**
  * **Slider:** Navigasi penggeser waktu maju-mundur secara dinamis.
  * **Kalender:** Tampilan kalender dengan penanda tanggal-tanggal transit penting.
  * **Pencari Momen Penting (*Aspect Hit Scanner*):** Fitur pencari otomatis untuk melompat langsung ke tanggal terjadinya transit-transit penting.

### Fitur 4: Fitur Bagikan (*Share Feature*)
* Pengguna dapat membagikan bagan (*chart*) dan hasil analisisnya ke pengguna lain atau ke platform luar.

### Fitur 5: Kecocokan Multi-Relasi (*Compatibility / Synastry*)
* Penilaian kecocokan tidak terbatas pada hubungan pasangan romantis saja, melainkan mencakup:
  * **Pasangan** (*Romantic / Partner*)
  * **Teman** (*Friendship*)
  * **Rekan Kerja / Bisnis** (*Professional / Coworker*)
* **Sumber Profil yang Dicocokkan:**
  * Berdasarkan **Kontak HP**.
  * Berdasarkan **Orang di Sekitar (*Nearby / Proximity*)**.
  * Berdasarkan **Orang Tidak Dikenal:** Seluruh analisis dan dimensi kecocokan tetap ditampilkan secara lengkap dan menyeluruh.

### Fitur 6: Chatbot AI dengan Fitur RAG (*Retrieval-Augmented Generation*)
* Karena data astronomis yang dihasilkan kalkulator masih sangat mentah (*raw data*), disediakan asisten **Chatbot bertenaga RAG**.
* **Fungsi RAG:** Mengambil teks referensi/doktrin otoritatif yang terpercaya dan menggabungkannya dengan data mentah posisi planet pengguna, untuk menghasilkan penjelasan yang manusiawi tanpa halusinasi dan tanpa Barnum effect.

---

## 3. Catatan Pemilihan Fase

Seluruh poin di atas adalah **fitur yang diinginkan**. Pada tahap berikutnya, daftar ini akan dipilah bersama pengguna untuk menentukan:
* **Fase 1 (Fondasi Awal / MVP):** Fitur inti yang wajib ada pertama kali agar sistem bisa berjalan.
* **Fase Berikutnya:** Fitur lanjutan yang akan dikembangkan secara bertahap.

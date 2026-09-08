# Pengetahuan Domain: Dasar-Dasar Astrologi (Domain Knowledge)

Dokumen ini adalah fondasi konseptual sistem astrologi untuk pengembang perangkat lunak dan basis pengetahuan (*Knowledge Base*) untuk sistem AI/RAG. Dokumen ini mendefinisikan terminologi, mekanika fisik langit, dan aturan penalaran tanpa mistisisme.

---

## 1. Definisi Mekanis Astrologi

Secara teknis, sebuah bagan astrologi (*birth chart / natal chart*) adalah **proyeksi snapshot geometri 2D dari tata surya dilihat dari titik koordinat fisik permukaan bumi pada detik waktu tertentu**.

Sistem astrologi beroperasi di atas **4 Pilar Utama (Analogi Panggung Teater)**:

```
+-------------------------------------------------------------------------+
|                          4 PILAR UTAMA ASTROLOGI                        |
|                                                                         |
|  1. PLANET       -> Aktor      ("Fungsi mental apa yang bekerja?")      |
|  2. ZODIAK       -> Kostum     ("Bagaimana gaya ekspresi energinya?")   |
|  3. RUMAH        -> Panggung   ("Di area hidup mana hal ini terjadi?")  |
|  4. ASPEK SUDUT  -> Dialog     ("Bagaimana interaksi antar-planet?")    |
+-------------------------------------------------------------------------+
```

---

## 2. Pilar I: Planet (*The Actors - "WHO / WHAT"*)

Planet merepresentasikan penggerak arketipal dan fungsi psikologis manusia:

| Planet / Titik | Simbol Arketipe | Fungsi Psikologis & Representasi |
| :--- | :--- | :--- |
| **Matahari (*Sun / Surya*)** | Sang Raja / Jiwa | Ego sadar, identitas inti, kehendak (*willpower*), vitalitas fisik. |
| **Bulan (*Moon / Chandra*)** | Sang Ratu / Pikiran | Pikiran bawah sadar (*Manas*), rasa aman emosional, insting, memori. |
| **Merkurius (*Mercury / Budha*)** | Sang Utusan / Pemikir | Logika analitis (*Buddhi*), pemrosesan data, bicara, komunikasi, adaptasi. |
| **Venus (*Shukra*)** | Sang Seniman / Pecinta | Nilai diri (*self-worth*), estetika, gaya relasi, daya tarik personal. |
| **Mars (*Mangala*)** | Sang Panglima / Pejuang | Daya dorong eksekusi, inisiatif aksi, agresi, keberanian, energi fisik. |
| **Jupiter (*Guru*)** | Sang Guru / Filosof | Kebijaksanaan moral, ekspansi wawasan, optimisme, keberuntungan etis. |
| **Saturnus (*Shani*)** | Sang Penguji / Pertapa | Realitas batas, disiplin baja, rasa takut, tanggung jawab, ujian waktu. |
| **Uranus** | Sang Pemberontak | Terobosan mendadak, independensi radikal, ketegangan neuro-elektrik. |
| **Neptunus** | Sang Mistikus | Imajinasi tinggi, batas ego yang melebur, spiritualitas, ilusi vs intuisi. |
| **Pluto** | Sang Transformator | Kekuasaan bawah tanah, regenerasi radikal, eliminasi hal-hal usang. |
| **Rahu (North Node)** | Kepala Naga | Obsesi masa depan, ambisi material, eksplorasi hal asing/tidak konvensional. |
| **Ketu (South Node)** | Ekor Naga | Pelepasan (*detachment*), asketisme, bakat bawaan masa lalu, spiritualitas. |

---

## 3. Pilar II: Zodiak (*The Costumes - "HOW"*)

Zodiak adalah sabuk ekliptika 360 derajat yang dibagi menjadi 12 bagian sama besar ($30^\circ$ per zodiak). Zodiak menentukan **warna, temperamen, dan modalitas** cara planet bertindak.

### 3.1 Pembagian Berdasarkan 4 Elemen:
1. **Api (Aries, Leo, Sagittarius):** Antusias, ekspresif, berorientasi aksi, percaya diri.
2. **Tanah (Taurus, Virgo, Capricorn):** Praktis, realistis, stabil, berorientasi bukti nyata dan materi.
3. **Udara (Gemini, Libra, Aquarius):** Intelektual, objektif, komunikatif, berorientasi gagasan dan sosial.
4. **Air (Cancer, Scorpio, Pisces):** Intuitif, emosional, peka, berorientasi rasa batin dan empati.

### 3.2 Pembagian Berdasarkan 3 Modalitas:
1. **Kardinal (Aries, Cancer, Libra, Capricorn):** Inisiator, perintis, memulai sesuatu yang baru.
2. **Tetap / Fixed (Taurus, Leo, Scorpio, Aquarius):** Menjaga kestabilan, konsisten, ulet, resisten terhadap perubahan.
3. **Mutabel (Gemini, Virgo, Sagittarius, Pisces):** Adaptif, fleksibel, mudah beralih, jembatan transisi.

---

## 4. Pilar III: Rumah (*The Stage - "WHERE"*)

Rumah (*Houses / Bhava*) membagi 24 jam rotasi bumi menjadi 12 sektor kehidupan. Titik tolak perhitungan rumah dimulai dari **Ascendant (Lagna)**, yaitu zodiak dan derajat yang sedang terbit di ufuk timur pada detik kelahiran.

* **Rumah 1 (*Tanu Bhava / Lagna*):** Diri fisik, kepribadian tampak luar, vitalitas tubuh, cara pandang hidup.
* **Rumah 2 (*Dhana Bhava*):** Keuangan pribadi, aset material, tutur kata, keluarga masa kecil.
* **Rumah 3 (*Sahaja Bhava*):** Komunikasi harian, keterampilan teknis, keberanian (*parakrama*), relasi saudara.
* **Rumah 4 (*Sukha Bhava*):** Kedamaian batin, rumah/properti, figur ibu, rasa nyaman emosional.
* **Rumah 5 (*Putra Bhava*):** Kreativitas murni, kecerdasan spekulatif, anak, romantisme, pahala karma baik (*purva punya*).
* **Rumah 6 (*Ari Bhava*):** Rutinitas kerja, hambatan, konflik, utang, kesehatan fisik, daya mengatasi rintangan.
* **Rumah 7 (*Yuvati Bhava*):** Pasangan hidup, kemitraan bisnis, hubungan satu-lawan-satu (*the significant other*).
* **Rumah 8 (*Randhra Bhava*):** Krisis, kematian/kelahiran kembali, uang bersama/warisan, misteri, transformasi radikal.
* **Rumah 9 (*Dharma Bhava*):** Filsafat hidup, etika, pendidikan tinggi, perjalanan jauh, figur ayah/guru pembimbing.
* **Rumah 10 (*Karma Bhava / MC*):** Puncak karier, reputasi sosial, kontribusi publik, otoritas profesional.
* **Rumah 11 (*Labha Bhava*):** Komunitas besar, jejaring sosial, cita-cita jangka panjang, keuntungan finansial (*gains*).
* **Rumah 12 (*Vyaya Bhava*):** Pengeluaran, isolasi privat, ruang bawah sadar, spiritualitas, tidur, pelepasan duniawi.

---

## 5. Pilar IV: Aspek Geometri (*The Dialogue / Interaction*)

Aspek adalah jarak sudut ($\Delta\theta$) antar planet pada lingkaran 360 derajat.

* **Konjungsi ($0^\circ$):** Penggabungan/peleburan dua energi planet menjadi satu dorongan utuh.
* **Oposisi ($180^\circ$):** Tarik-menarik polaritas; sering diproyeksikan keluar ke figur orang lain.
* **Square ($90^\circ$):** Sudut siku tegangan (*friction*); memicu krisis internal yang memaksa aksi nyata.
* **Trine ($120^\circ$):** Aliran harmonis alami; bakat bawaan yang bekerja tanpa perlawanan.
* **Sextile ($60^\circ$):** Peluang kerja sama yang membutuhkan stimulasi aktif untuk berbuah.

---

## 6. Komparasi Fundamental: Astrologi Barat vs Astrologi India

| Parameter Teknis | Astrologi Barat (Tropical / Sayana) | Astrologi India (Vedic / Sidereal / Nirayana) |
| :--- | :--- | :--- |
| **Kerangka Referensi** | **Musim Bumi (Equinox).** $0^\circ$ Aries selalu dikunci pada titik awal musim semi matahari. | **Bintang Nyata (Sidereal).** Menghitung pergeseran presesi sumbu bumi (*Ayanamsha* $\approx 24^\circ$). |
| **Fokus Analisis** | **Arsitektur Psikologis.** Menelaah struktur ego, luka batin, motivasi bawah sadar, dan integrasi diri. | **Waktu & Takdir (*Kala & Karma*).** Memetakan siklus waktu kapan potensi benih hidup akan berbuah. |
| **Fitur Khas** | Pola aspek geometri rumit (T-Square, Grand Trine, Yod) dan asteroid modern. | **27 Nakshatra** (bintang mikro), **Divisional Charts (D9 Navamsha)**, dan **Vimshottari Dasha** (jam waktu hidup). |

---

## 7. Prinsip Rekayasa Sistem: Eliminasi Efek Barnum (*Zero Sycophancy*)

Untuk mencegah sistem menghasilkan teks ramalan generik (*Barnum / Forer effect*), seluruh interpretasi wajib menaati prinsip:

1. **Aturan Kausalitas Posisi:** Setiap narasi interpretasi harus dapat dirunut kembali ke rumus:
   $$\text{Interpretasi} = f(\text{Planet}, \text{Zodiak}, \text{Rumah}, \text{Aspek Terbobot}, \text{Dasha})$$
2. **Larangan Ambiguitas Universal:** Dilarang menggunakan frasa yang berlaku bagi semua manusia (misal: *"Anda terkadang ragu tapi ingin maju"*).
3. **Keseimbangan Obyektif:** Jika aspek transit yang terbentuk adalah tegangan keras pada penguasa siklus Dasha musuh (*Maha Shatru*), sistem wajib memaparkan friksi tersebut secara terbuka tanpa pemanis kata.

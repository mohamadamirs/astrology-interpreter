# ADR-0007: Arsitektur RAG dan Basis Data Vektor Doktrin Klasik

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Untuk memenuhi mandat PRD mengenai penolakan Efek Barnum dan larangan halusinasi, sistem AI Chatbot tidak boleh menghasilkan teks interpretasi bebas tanpa rujukan. Sistem memerlukan arsitektur *Retrieval-Augmented Generation* (RAG) yang membumikan jawaban pada teks klasik otoritatif (misal: *Brihat Parashara Hora Shastra*, *Phaladeepika*, risalah Ptolemaik).

Pilihan yang dievaluasi:
1. **Fine-tuning LLM secara langsung:** Mahal, rawan halusinasi (*catastrophic forgetting*), dan sulit diaudit sumbernya.
2. **Hardcoded Rules-Engine:** Kaku, membutuhkan penulisan jutaan kombinasi manual, dan pengalaman pengguna terbatas.
3. **Hybrid RAG Pipeline (pgvector / ChromaDB + Low-Temperature LLM):** Menyimpan potongan teks klasik dalam basis data vektor, melakukan pencarian kemiripan semantik berdasarkan konfigurasi transit/natal, dan menyuntikkannya sebagai konteks *ground truth*.

## Keputusan
Memilih **Hybrid RAG Pipeline** dengan kriteria:
1. Potongan dokumen klasik di-indeks dengan embedding semantik dan metadata terstruktur (planet, tanda, rumah, jenis aspek, domain hidup).
2. Inferensi LLM diatur pada *temperature low* (0.2) dengan instruksi sistem ketat yang mewajibkan sitasi bab dan melarang kalimat sanjungan generik (*flattery bias*).
3. Jika skor kemiripan vektor di bawah ambang batas ($< 0.65$), model wajib menyatakan secara transparan bahwa konfigurasi tersebut tidak memiliki padanan dalam doktrin klasik.

## Konsekuensi
* **Positif:** 0% Halusinasi doktrin, transparansi sitasi penuh, dan kepatuhan mutlak pada prinsip anti-Barnum.
* **Trade-off:** Memerlukan proses kurasi dan chunking teks literatur klasik di awal serta infrastruktur basis data vektor.

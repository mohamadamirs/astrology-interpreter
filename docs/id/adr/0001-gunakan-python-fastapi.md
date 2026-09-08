# ADR-0001: Pemilihan Python (FastAPI) sebagai Engine Inti Efemeris & Komputasi

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Sistem membutuhkan backend yang mampu menghitung mekanika benda langit sub-detik busur, konversi Julian Date, matriks presesi Ayanamsha, dan siklus rekursif Dasha.

Pilihan yang dievaluasi:
1. **Python (FastAPI + PyEphem / Swiss Ephemeris)**
2. **Node.js / TypeScript (astronomy-engine / addon C++)**
3. **Go (Porting astronomi manual)**

## Keputusan
Memilih **Python dengan FastAPI** karena:
1. **Kematangan Ekosistem:** Library astronomis Python (`ephem`, `pyswisseph`) adalah standar industri yang telah diaudit langsung terhadap vektor NASA JPL Horizons.
2. **Kinerja Asinkron:** FastAPI (ASGI Uvicorn) memberikan throughput I/O tinggi setara Node.js dengan kapabilitas komputasi numerik bawaan C/Python.
3. **Kontrak Ketat:** Pydantic v2 memberikan validasi skema otomatis dan dokumen OpenAPI 3.1.

## Konsekuensi
* **Positif:** Presisi komputasi terjamin; pengembangan model matematika cepat dan minim bug.
* **Trade-off:** Arsitektur multi-bahasa (Python di backend, TypeScript di frontend).

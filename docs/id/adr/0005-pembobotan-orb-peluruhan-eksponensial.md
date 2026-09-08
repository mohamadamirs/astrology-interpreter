# ADR-0005: Pembobotan Orb Aspek via Fungsi Peluruhan Eksponensial Kontinu

* **Status:** Disetujui (Accepted)  
* **Tanggal:** 2026-09-08  

## Konteks & Masalah
Tabel batas orb konvensional (misal $< 1^\circ$ Kuat, $> 1^\circ$ Lemah) menciptakan anomali lonjakan skor ekstrem (*cliff-edge jump*) hanya karena selisih $0.01^\circ$.

## Keputusan
Menerapkan **Fungsi Peluruhan Eksponensial Kontinu**:
$$W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$$
* Aspek eksak ($\delta = 0.00^\circ$): $W = 10.00$
* Aspek dekat ($\delta = 0.50^\circ$): $W = 4.96$
* Aspek longgar ($\delta = 3.00^\circ$): $W = 0.15$ (Diabaikan)
* Pengali $1.5\times$ diterapkan jika aspek menyentuh penguasa Mahadasha atau Antardasha yang sedang aktif.

## Konsekuensi
* **Positif:** Kurva dinamika skor harian mulus, kontinu, dan secara realistis melipatgandakan dampak aspek eksak.
* **Trade-off:** Perhitungan non-linear sedikit lebih rumit dibandingkan tabel integer sederhana.

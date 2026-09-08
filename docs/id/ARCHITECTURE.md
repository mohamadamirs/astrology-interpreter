# Arsitektur Teknis & Desain Sistem

## 1. Topologi Sistem

Arsitektur komputasi tanpa status (*stateless*) dan terpisah (*decoupled*):
* **Backend:** Python (FastAPI) menangani komputasi matematika astronomis, lookup zona waktu spasial offline, dan penilaian deterministik.
* **Frontend:** Universal React Native (Expo) menargetkan Android, iOS, dan Web (SPA) via `react-native-web`.
* **Database:** PostgreSQL (Produksi) / SQLite (Pengembangan) dengan ORM SQLAlchemy 2.0.

```
[ Klien Expo (iOS / Android / Web) ]
   ├── LocationPicker (expo-location + react-native-maps)
   ├── ChartCanvas (react-native-svg)
   └── Store (Zustand + TanStack Query)
                 │  HTTPS JSON REST
                 ▼
[ Backend FastAPI (Python) ]
   ├── GeoTimeService (timezonefinder + zoneinfo)
   ├── EphemerisService (pyephem / pyswisseph)
   ├── JyotishEngine (Nakshatra, Pada, Sub-Lord KP, Dignity)
   ├── DashaEngine (Vimshottari 4 lapis hierarkis)
   ├── TransitEngine (Aspek + Peluruhan Eksponensial)
   └── ScoringEngine (Akumulator 5-Domain)
                 │
                 ▼
[ PostgreSQL / SQLite ]
```

---

## 2. Struktur Direktori

```text
backend/
├── app/
│   ├── api/v1/endpoints/     # geo.py, chart.py, transits.py, interpret.py
│   ├── core/                 # config.py, constants.py, exceptions.py
│   ├── engine/               # LOGIKA ASTRONOMIS MURNI (Bebas dependensi web)
│   │   ├── ephemeris.py      # Bujur/lintang/kecepatan & logika retrograde
│   │   ├── ayanamsha.py      # Lahiri, KP, Raman, Fagan-Bradley
│   │   ├── angles.py         # RAMC, Ascendant, Midheaven, House Cusps
│   │   ├── jyotish.py        # Nakshatras, Padas, Sub-Lords KP, Dignity
│   │   ├── dasha.py          # Kalkulasi MD/AD/PD/SD Vimshottari
│   │   ├── aspects.py        # Separasi sudut & pembobotan eksponensial
│   │   └── scoring.py        # Matriks skor kuantitatif 5-domain
│   ├── models/               # Model SQLAlchemy (User, SavedChart, TransitCache)
│   ├── schemas/              # Skema validasi Pydantic request/response
│   └── services/             # Layanan orkestrasi
└── tests/                    # Pengujian pytest + vektor benchmark ground truth

frontend/
├── src/
│   ├── api/                  # Klien Axios & hook TanStack Query
│   ├── components/           # Button, Card, Modal, Typography
│   ├── features/
│   │   ├── location-picker/  # Tombol GPS & pemilih pin peta interaktif
│   │   ├── chart-viewer/     # SVG bagan India Selatan/Utara & roda Barat
│   │   ├── domain-barometer/ # Kartu gauge & penampil vonis objektif
│   │   └── natal-form/       # Input tanggal/jam & sakelar zodiak
│   └── store/                # State klien Zustand
└── app/                      # Rute layar Expo Router
```

---

## 3. Pipa Alur Matematika Inti

### 3.1 Pipa Geospasial & UTC Historis
1. Terima $(Lat, Lon)$ $\rightarrow$ Kueri `timezonefinder` secara offline $\rightarrow$ Dapatkan string IANA (misal `Asia/Jakarta`).
2. Tentukan datetime sipil lokal via `zoneinfo.ZoneInfo(tz_name)` $\rightarrow$ Otomatis hitung offset DST historis $\rightarrow$ Dapatkan timestamp UTC kanonikal.

### 3.2 Pipa Ascendant & Proyeksi Ekliptika
1. Hitung Greenwich Sidereal Time ($GST$) dari Julian Date $JD$.
2. Hitung Waktu Sideris Lokal: $\theta_L = (GST + \text{lon}) \pmod{360^\circ}$.
3. Hitung Ascendant:
   $$\tan(\text{Asc}) = \frac{\cos(\theta_L)}{-\sin(\theta_L)\cos(\epsilon) - \tan(\phi)\sin(\epsilon)}$$
4. Hitung Bujur Sidereal: $\lambda_{\text{sidereal}} = (\lambda_{\text{tropikal}} - \text{Ayanamsha}) \pmod{360^\circ}$.

### 3.3 Pipa Penelusuran Vimshottari
1. Ambil Bujur Sidereal Bulan ($\lambda_{\text{Bulan}}$) dan temukan indeks Nakshatra.
2. Tentukan fraksi yang terlewati dan sisa masa penguasa Nakshatra saat lahir.
3. Maju menelusuri array siklus `[Ketu(7), Venus(20), Sun(6), Moon(10), Mars(7), Rahu(18), Jupiter(16), Saturn(19), Mercury(17)]` untuk mengisolasi batas MD, AD, PD, dan SD pada tanggal target.

### 3.4 Pipa Pembobotan Aspek Kontinu
Untuk aspek transit dengan selisih sudut $\delta$ (orb dalam derajat):
$$W(\delta) = 10.0 \times \exp(-1.4 \times \delta)$$
Terapkan pengali $W_{\text{efektif}} = W(\delta) \times 1.5$ jika aspek mengenai penguasa MD atau AD aktif.

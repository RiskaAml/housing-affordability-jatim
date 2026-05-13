# 🏠 Housing Affordability Dashboard — Jawa Timur 2020–2025

## Setup (VS Code)

### 1. Buat folder project
```
housing-dashboard/
├── app.py
├── ANALISIS_KETERJANGKAUAN_KPR.xlsx
└── requirements.txt
```

### 2. Install dependencies
Buka terminal di VS Code, jalankan:
```bash
pip install streamlit plotly pandas openpyxl requests
```

### 3. Jalankan dashboard
```bash
streamlit run app.py
```
Browser otomatis buka di `http://localhost:8501`

## Fitur Dashboard
- 🗺️ Peta interaktif per kabupaten/kota
- 📊 Bar chart UMK vs cicilan KPR
- 📈 Tren UMK 2020–2025
- 📉 IHPR Surabaya
- 🏡 Kepemilikan rumah & komposisi pekerja
- 📋 Tabel + download CSV

## Filter
- Pilih tahun (2020–2025)
- Perspektif Lajang / Keluarga Kecil
- Pilih kabupaten/kota spesifik

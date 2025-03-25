# ecommerce-analysis

Proyek ini bertujuan untuk menganalisis data e-commerce dari Olist dan menyajikan hasilnya melalui **dashboard interaktif** menggunakan **Streamlit**.

## 📌 Setup Virtual Environment

Disarankan untuk menggunakan **virtual environment** agar dependensi proyek tetap terkelola dengan baik. Ikuti langkah-langkah berikut:

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

## 📦 Instalasi Dependencies

Semua dependencies yang diperlukan telah disimpan dalam berkas `requirements.txt`. Install dengan perintah berikut:

```bash
pip install -r requirements.txt
```

## 🚀 Menjalankan Dashboard

Pastikan virtual environment sudah aktif, lalu jalankan dashboard dengan perintah berikut:

```bash
streamlit run dashboard/dashboard.py
```

## 📂 Struktur Direktori

```
📦 ecommerce-analysis
├── 📂 dashboard
│   ├── dashboard.py           # Kode utama Streamlit Dashboard
│   ├── main_data.csv          # Dataset utama yang digunakan
├── 📂 data
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── ... (dataset lainnya)
├── README.md                  # Dokumentasi proyek
├── notebook.ipynb              # Notebook eksplorasi data
├── requirements.txt            # Daftar dependencies
└── url.txt                     # Referensi data
```

## 🔗 Referensi Data

Dataset berasal dari **Olist** dan dapat diakses melalui tautan berikut:
- [Olist E-commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

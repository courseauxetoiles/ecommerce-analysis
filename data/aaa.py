import pandas as pd

# 🔹 Load Data
main_data_path = "main_data.csv"
geolocation_path = "D:\Bootcamp\Dicoding-ML Engineer\ecommerce-analysis\ecommerce-analysis-main\data\olist_customers_dataset.csv"

df_main = pd.read_csv(main_data_path - 'D:\Bootcamp\Dicoding-ML Engineer\ecommerce-analysis\ecommerce-analysis-main\data\olist_geolocation_dataset.csv')
df_geo = pd.read_csv(geolocation_path)

# 🔹 Pastikan kolom yang digunakan untuk join tersedia
if "customer_zip_code_prefix" not in df_main.columns:
    raise ValueError("Kolom 'customer_zip_code_prefix' tidak ditemukan di main_data.csv.")

if "geolocation_zip_code_prefix" not in df_geo.columns:
    raise ValueError("Kolom 'geolocation_zip_code_prefix' tidak ditemukan di olist_geolocation_dataset.csv.")

# 🔹 Drop duplikasi kode pos di geolocation untuk menghindari multiple join
df_geo = df_geo.groupby("geolocation_zip_code_prefix").agg({
    "geolocation_lat": "mean",
    "geolocation_lng": "mean",
    "geolocation_city": "first",
    "geolocation_state": "first"
}).reset_index()

# 🔹 Gabungkan data geolocation berdasarkan kode pos pelanggan
df_main = df_main.merge(
    df_geo,
    left_on="customer_zip_code_prefix",
    right_on="geolocation_zip_code_prefix",
    how="left"
)

# 🔹 Hapus kolom duplikat setelah merge
df_main.drop(columns=["geolocation_zip_code_prefix"], inplace=True)

# 🔹 Simpan dataset baru ke file CSV
df_main.to_csv("main_data_updated.csv", index=False)

print("✅ Data geolocation berhasil ditambahkan ke main_data_updated.csv!")

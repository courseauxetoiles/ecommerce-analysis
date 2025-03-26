import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ========================== 1️⃣ LOAD DATA ==========================
st.title("📊 E-Commerce Analysis Dashboard")

# Pastikan file tersedia sebelum memuat data
file_path = os.path.join(os.path.dirname(__file__), "main_data.csv")

if not os.path.exists(file_path):
    st.error("⚠️ File 'main_data.csv' tidak ditemukan. Pastikan file tersedia di repo GitHub!")
    st.stop()

df = pd.read_csv(file_path, parse_dates=["order_purchase_timestamp"])

# Isi NaN dengan nilai default agar tidak error
df.fillna(0, inplace=True)

# ========================== 2️⃣ SIDEBAR MENU & FILTER ==========================
st.sidebar.title("🔍 Pilih Analisis")
option = st.sidebar.radio("Pilih Analisis:", [
    "Overview Data", "RFM Analysis", "Distribusi Geografis", "Kategori Produk"
])

# **FILTER: Rentang Waktu**
min_date = df["order_purchase_timestamp"].min().date()
max_date = df["order_purchase_timestamp"].max().date()
date_range = st.sidebar.slider("Pilih Rentang Waktu:", min_date, max_date, (min_date, max_date))
df_filtered = df[(df["order_purchase_timestamp"].dt.date >= date_range[0]) &
                 (df["order_purchase_timestamp"].dt.date <= date_range[1])]

# **FILTER: Status Pesanan**
order_status = st.sidebar.multiselect("Pilih Status Pesanan:", df["order_status"].unique(), default=df["order_status"].unique())
df_filtered = df_filtered[df_filtered["order_status"].isin(order_status)]

# **FILTER: Warna Tema Visualisasi**
color_themes = {
    "Dark": "plotly_dark",
    "Light": "plotly_white",
    "Solar": "solar",
    "Seaborn": "seaborn"
}
selected_theme = st.sidebar.selectbox("Pilih Tema Visualisasi:", list(color_themes.keys()))

# ========================== 3️⃣ OVERVIEW DATA ==========================
if option == "Overview Data":
    st.header("📊 Overview Data")

    col1, col2 = st.columns(2)
    col1.metric("Total Pelanggan", df_filtered["customer_id"].nunique())
    col2.metric("Total Pesanan", df_filtered.shape[0])

    # 🎯 Tren Jumlah Pesanan Per Bulan
    df_filtered["order_month"] = df_filtered["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_orders = df_filtered.groupby("order_month")["order_id"].count().reset_index()

    fig_tren_bulanan = px.line(
        monthly_orders, 
        x="order_month", 
        y="order_id", 
        markers=True, 
        title="📈 Tren Jumlah Pesanan Per Bulan",
        template=color_themes[selected_theme]
    )
    fig_tren_bulanan.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Jumlah Pesanan",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig_tren_bulanan, use_container_width=True)

# ========================== 4️⃣ RFM ANALYSIS ==========================
elif option == "RFM Analysis":
    st.header("📈 RFM Analysis")

    required_columns = ["customer_id", "recency", "frequency", "monetary", "Segment"]
    if not all(col in df_filtered.columns for col in required_columns):
        st.error("⚠️ Data RFM tidak ditemukan. Pastikan kolom tersedia dalam dataset.")
        st.stop()

    # **FILTER: Segmentasi Pelanggan**
    selected_segment = st.sidebar.multiselect("Pilih Segmentasi RFM:", df_filtered["Segment"].unique(), default=df_filtered["Segment"].unique())
    df_filtered = df_filtered[df_filtered["Segment"].isin(selected_segment)]

    rfm = df_filtered.groupby("customer_id").agg(
        recency=("recency", "min"),
        frequency=("frequency", "sum"),
        monetary=("monetary", "sum")
    ).reset_index()

    # 🎯 Distribusi Recency, Frequency, Monetary
    fig_rfm_recency = px.histogram(rfm, x="recency", nbins=30, title="Distribusi Recency", template=color_themes[selected_theme])
    fig_rfm_frequency = px.histogram(rfm, x="frequency", nbins=30, title="Distribusi Frequency", template=color_themes[selected_theme])
    fig_rfm_monetary = px.histogram(rfm, x="monetary", nbins=30, title="Distribusi Monetary", template=color_themes[selected_theme])

    st.plotly_chart(fig_rfm_recency, use_container_width=True)
    st.plotly_chart(fig_rfm_frequency, use_container_width=True)
    st.plotly_chart(fig_rfm_monetary, use_container_width=True)

# ========================== 5️⃣ DISTRIBUSI GEOGRAFIS ==========================
elif option == "Distribusi Geografis":
    st.header("🌍 Distribusi Geografis Pesanan")

    if not all(col in df_filtered.columns for col in ["geolocation_lat", "geolocation_lng"]):
        st.error("⚠️ Data lokasi pelanggan tidak ditemukan dalam main_data.csv.")
        st.stop()

    # 🎯 Scatter Plot Hubungan Jarak dan Waktu Pengiriman
    fig_scatter = px.scatter(
        df_filtered,
        x="geolocation_lat",
        y="geolocation_lng",
        color="delivery_time",
        title="Hubungan Jarak dan Waktu Pengiriman",
        template=color_themes[selected_theme],
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ========================== 6️⃣ KATEGORI PRODUK ==========================
elif option == "Kategori Produk":
    st.header("🛍️ Kategori Produk dengan Penjualan Tertinggi")

    if "product_category_name_english" not in df_filtered.columns:
        st.error("⚠️ Data kategori produk tidak ditemukan.")
        st.stop()

    category_sales = df_filtered["product_category_name_english"].value_counts().head(10).reset_index()
    category_sales.columns = ["Kategori Produk", "Jumlah Penjualan"]

    fig_category = px.bar(
        category_sales,
        x="Kategori Produk",
        y="Jumlah Penjualan",
        title="Top 10 Kategori Produk dengan Penjualan Tertinggi",
        template=color_themes[selected_theme],
        color="Jumlah Penjualan"
    )
    st.plotly_chart(fig_category, use_container_width=True)

    # 🎯 Tren Penjualan Bulanan per Kategori Produk
    df_filtered["order_month"] = df_filtered["order_purchase_timestamp"].dt.to_period("M").astype(str)
    category_monthly_sales = df_filtered.groupby(["order_month", "product_category_name_english"])["order_id"].count().reset_index()

    fig_category_trend = px.line(
        category_monthly_sales,
        x="order_month",
        y="order_id",
        color="product_category_name_english",
        title="📈 Tren Penjualan Bulanan per Kategori Produk",
        template=color_themes[selected_theme],
        markers=True
    )

    st.plotly_chart(fig_category_trend, use_container_width=True)

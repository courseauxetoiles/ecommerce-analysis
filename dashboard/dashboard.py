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

# ========================== 2️⃣ SIDEBAR MENU ==========================
st.sidebar.title("🔍 Pilih Analisis")
option = st.sidebar.radio("Pilih Analisis:", ["Overview Data", "RFM Analysis", "Distribusi Geografis"])

# ========================== 3️⃣ OVERVIEW DATA ==========================
if option == "Overview Data":
    st.header("📊 Overview Data")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Pelanggan", df["customer_id"].nunique())
    col2.metric("Total Pesanan", df.shape[0])
    
    # Fitur interaktif: Filter berdasarkan rentang tanggal
    df["order_day"] = df["order_purchase_timestamp"].dt.date
    min_date = df["order_day"].min()
    max_date = df["order_day"].max()

    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    df_filtered = df[(df["order_day"] >= start_date) & (df["order_day"] <= end_date)]
    daily_counts = df_filtered.groupby("order_day").size().reset_index(name="jumlah_pesanan")

    fig_daily = px.line(daily_counts, x="order_day", y="jumlah_pesanan",
                        title="📈 Tren Pesanan Harian", template="plotly_dark")
    st.plotly_chart(fig_daily, use_container_width=True)

    df_filtered["order_month_str"] = df_filtered["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_counts = df_filtered.groupby("order_month_str").size().reset_index(name="jumlah_pesanan")

    fig_monthly = px.bar(monthly_counts, x="order_month_str", y="jumlah_pesanan",
                         title="📅 Tren Pesanan Bulanan", template="plotly_dark")
    st.plotly_chart(fig_monthly, use_container_width=True)

# ========================== 4️⃣ RFM ANALYSIS ==========================
elif option == "RFM Analysis":
    st.header("📈 RFM Analysis")

    # Cek apakah kolom yang diperlukan ada
    required_columns = ["customer_id", "recency", "frequency", "monetary"]
    if not all(col in df.columns for col in required_columns):
        st.error("⚠️ Data RFM tidak ditemukan. Pastikan kolom 'recency', 'frequency', dan 'monetary' tersedia dalam CSV.")
        st.stop()
    
    rfm = df.groupby("customer_id").agg(
        recency=("recency", "min"),
        frequency=("frequency", "sum"),
        monetary=("monetary", "sum")
    ).reset_index()

    # Fitur interaktif: Filter berdasarkan kategori pelanggan
    rfm["Kategori"] = pd.cut(
        rfm["recency"],
        bins=[0, 30, 90, 180, 365, float("inf")],
        labels=["Loyal", "Potensial", "Baru", "Berisiko", "Hilang"]
    )

    kategori_pilihan = st.sidebar.selectbox("Pilih Kategori Pelanggan", rfm["Kategori"].unique())
    rfm_filtered = rfm[rfm["Kategori"] == kategori_pilihan]

    fig_rfm = px.scatter(rfm_filtered, x="recency", y="frequency", size="monetary", color="monetary",
                         title=f"📊 Scatter Plot RFM - {kategori_pilihan}", template="plotly_dark")
    st.plotly_chart(fig_rfm, use_container_width=True)

# ========================== 5️⃣ DISTRIBUSI GEOGRAFIS ==========================
elif option == "Distribusi Geografis":
    st.header("🌍 Distribusi Geografis Pesanan")
    
    # Cek apakah kolom customer_city ada
    if "customer_city" not in df.columns:
        st.error("⚠️ Data kota pelanggan tidak ditemukan.")
        st.stop()
    
    # Fitur interaktif: Pilih jumlah kota yang ingin ditampilkan
    top_n = st.sidebar.slider("Tampilkan Top N Kota", min_value=5, max_value=20, value=10)

    top_cities = df["customer_city"].value_counts().head(top_n).reset_index()
    top_cities.columns = ["customer_city", "jumlah_pesanan"]

    fig_geo = px.bar(top_cities, x="customer_city", y="jumlah_pesanan",
                     title=f"🏙️ Top {top_n} Kota dengan Pesanan Terbanyak", template="plotly_dark")
    st.plotly_chart(fig_geo, use_container_width=True)

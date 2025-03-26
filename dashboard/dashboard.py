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

# ========================== 2️⃣ SIDEBAR MENU ==========================
st.sidebar.title("🔍 Pilih Analisis")
option = st.sidebar.radio("Pilih Analisis:", [
    "Overview Data", "RFM Analysis", "Distribusi Geografis", "Kategori Produk"
])

# ========================== 3️⃣ OVERVIEW DATA ==========================
if option == "Overview Data":
    st.header("📊 Overview Data")

    col1, col2 = st.columns(2)
    col1.metric("Total Pelanggan", df["customer_id"].nunique())
    col2.metric("Total Pesanan", df.shape[0])

    # 🎯 Tren Jumlah Pesanan Per Bulan
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_orders = df.groupby("order_month")["order_id"].count().reset_index()

    fig_tren_bulanan = px.line(
        monthly_orders, 
        x="order_month", 
        y="order_id", 
        markers=True, 
        title="📈 Tren Jumlah Pesanan Per Bulan",
        template="plotly_dark"
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
    if not all(col in df.columns for col in required_columns):
        st.error("⚠️ Data RFM tidak ditemukan. Pastikan kolom 'recency', 'frequency', 'monetary', dan 'Segment' tersedia.")
        st.stop()

    rfm = df.groupby("customer_id").agg(
        recency=("recency", "min"),
        frequency=("frequency", "sum"),
        monetary=("monetary", "sum")
    ).reset_index()

    # 🎯 Distribusi Recency, Frequency, Monetary
    fig_rfm_recency = px.histogram(rfm, x="recency", nbins=30, title="Distribusi Recency", template="plotly_dark")
    fig_rfm_frequency = px.histogram(rfm, x="frequency", nbins=30, title="Distribusi Frequency", template="plotly_dark")
    fig_rfm_monetary = px.histogram(rfm, x="monetary", nbins=30, title="Distribusi Monetary", template="plotly_dark")

    st.plotly_chart(fig_rfm_recency, use_container_width=True)
    st.plotly_chart(fig_rfm_frequency, use_container_width=True)
    st.plotly_chart(fig_rfm_monetary, use_container_width=True)

    # 🎯 Proporsi One-Time Buyers vs Repeat Customers
    one_time_buyers = (rfm["frequency"] == 1).sum()
    repeat_customers = len(rfm) - one_time_buyers

    fig_pie = px.pie(
        names=["One-Time Buyers", "Repeat Customers"],
        values=[one_time_buyers, repeat_customers],
        title="Proporsi One-Time Buyers vs Repeat Customers",
        color_discrete_sequence=["#ff9999", "#66b3ff"]
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # 🎯 Distribusi Segmen Pelanggan berdasarkan RFM
    segment_counts = df["Segment"].value_counts().reset_index()
    segment_counts.columns = ["Segment", "Jumlah Pelanggan"]

    fig_segment = px.bar(
        segment_counts,
        x="Segment",
        y="Jumlah Pelanggan",
        title="Distribusi Segmen Pelanggan berdasarkan RFM",
        template="plotly_dark"
    )
    st.plotly_chart(fig_segment, use_container_width=True)

# ========================== 5️⃣ DISTRIBUSI GEOGRAFIS ==========================
elif option == "Distribusi Geografis":
    st.header("🌍 Distribusi Geografis Pesanan")

    if not all(col in df.columns for col in ["geolocation_lat", "geolocation_lng"]):
        st.error("⚠️ Data lokasi pelanggan tidak ditemukan dalam main_data.csv.")
        st.stop()

    # 🎯 Scatter Plot Hubungan Jarak dan Waktu Pengiriman
    fig_scatter = px.scatter(
        df,
        x="geolocation_lat",
        y="geolocation_lng",
        color="delivery_time",
        title="Hubungan Jarak dan Waktu Pengiriman",
        template="plotly_dark",
        opacity=0.6
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ========================== 6️⃣ KATEGORI PRODUK ==========================
elif option == "Kategori Produk":
    st.header("🛍️ Kategori Produk dengan Penjualan Tertinggi")

    if "product_category_name_english" not in df.columns:
        st.error("⚠️ Data kategori produk tidak ditemukan.")
        st.stop()

    category_sales = df["product_category_name_english"].value_counts().head(10).reset_index()
    category_sales.columns = ["Kategori Produk", "Jumlah Penjualan"]

    fig_category = px.bar(
        category_sales,
        x="Kategori Produk",
        y="Jumlah Penjualan",
        title="Top 10 Kategori Produk dengan Penjualan Tertinggi",
        template="plotly_dark",
        color="Jumlah Penjualan"
    )
    st.plotly_chart(fig_category, use_container_width=True)

    # 🎯 Tren Penjualan Bulanan per Kategori Produk
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    category_monthly_sales = df.groupby(["order_month", "product_category_name_english"])["order_id"].count().reset_index()

    fig_category_trend = px.line(
        category_monthly_sales,
        x="order_month",
        y="order_id",
        color="product_category_name_english",
        title="📈 Tren Penjualan Bulanan per Kategori Produk",
        template="plotly_dark",
        markers=True
    )

    st.plotly_chart(fig_category_trend, use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv("main_data.csv", parse_dates=["order_purchase_timestamp"])
    return df

df = load_data()

st.sidebar.title("📊 Olist Dashboard")
option = st.sidebar.selectbox("Pilih Analisis:", ["Overview Data", "RFM Analysis", "Distribusi Geografis"])

# 1️⃣ OVERVIEW DATA
if option == "Overview Data":
    st.title("📊 Overview Data")
    
    col1, col2 = st.columns(2)
    col1.metric("Total Pelanggan", df["customer_id"].nunique())
    col2.metric("Total Pesanan", df.shape[0])
    
    df["order_day"] = df["order_purchase_timestamp"].dt.date
    daily_counts = df.groupby("order_day").size().reset_index(name="jumlah_pesanan")
    
    fig_daily = px.line(daily_counts, x="order_day", y="jumlah_pesanan", title="Tren Pesanan Harian", template="plotly_dark")
    st.plotly_chart(fig_daily, use_container_width=True)

    df["order_month_str"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    monthly_counts = df.groupby("order_month_str").size().reset_index(name="jumlah_pesanan")
    
    fig_monthly = px.bar(monthly_counts, x="order_month_str", y="jumlah_pesanan", title="Tren Pesanan Bulanan", template="plotly_dark")
    st.plotly_chart(fig_monthly, use_container_width=True)

# 2️⃣ RFM ANALYSIS
elif option == "RFM Analysis":
    st.title("📈 RFM Analysis")
    
    latest_date = df["order_purchase_timestamp"].max()
    rfm = df.groupby("customer_id").agg(
        recency=("recency", "min"),
        frequency=("frequency", "sum"),
        monetary=("monetary", "sum")
    ).reset_index()

    fig_rfm = px.scatter(rfm, x="recency", y="frequency", size="monetary", color="monetary", title="Scatter Plot RFM", template="plotly_dark")
    st.plotly_chart(fig_rfm, use_container_width=True)

# 3️⃣ DISTRIBUSI GEOGRAFIS
elif option == "Distribusi Geografis":
    st.title("🌍 Distribusi Geografsis Pesanan")
    
    top_cities = df["customer_city"].value_counts().head(10).reset_index()
    top_cities.columns = ["customer_city", "jumlah_pesanan"]
    
    fig_geo = px.bar(top_cities, x="customer_city", y="jumlah_pesanan", title="Top 10 Kota dengan Pesanan Terbanyak", template="plotly_dark")
    st.plotly_chart(fig_geo, use_container_width=True)

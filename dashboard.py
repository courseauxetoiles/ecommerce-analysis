import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("dashboard/main_data.csv", parse_dates=["order_purchase_timestamp"])

df = load_data()

# Sidebar
st.sidebar.title("📊 Olist Dashboard")
option = st.sidebar.selectbox("Pilih Analisis:", ["Overview Data", "RFM Analysis", "Distribusi Geografis"])

# Overview Data
if option == "Overview Data":
    st.title("📊 Overview Data")
    
    # Info dasar
    col1, col2 = st.columns(2)
    col1.metric("Total Pelanggan", df["customer_id"].nunique())
    col2.metric("Total Pesanan", df.shape[0])

    # Distribusi pesanan
    fig = px.histogram(df, x="order_purchase_timestamp", nbins=50, title="Distribusi Waktu Pesanan")
    st.plotly_chart(fig, use_container_width=True)

# RFM Analysis
elif option == "RFM Analysis":
    st.title("📈 RFM Analysis")
    
    latest_date = df["order_purchase_timestamp"].max()
    rfm = df.groupby("customer_id").agg(
        recency=("order_purchase_timestamp", lambda x: (latest_date - x.max()).days),
        frequency=("order_id", "count"),
        monetary=("payment_value", "sum")
    ).reset_index()

    # Visualisasi
    fig = px.histogram(rfm, x="recency", nbins=30, title="Distribusi Recency")
    st.plotly_chart(fig, use_container_width=True)

# Distribusi Geografis
elif option == "Distribusi Geografis":
    st.title("🌍 Distribusi Geografis Pesanan")
    
    top_cities = df["customer_city"].value_counts().head(10)
    fig = px.bar(top_cities, x=top_cities.index, y=top_cities.values, title="Top 10 Kota dengan Pesanan Terbanyak")
    st.plotly_chart(fig, use_container_width=True)

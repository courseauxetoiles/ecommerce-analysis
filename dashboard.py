import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Load datasets
@st.cache_data
def load_data():
    customers = pd.read_csv("olist_customers_dataset.csv")
    orders = pd.read_csv("olist_orders_dataset.csv", parse_dates=["order_purchase_timestamp"])
    order_items = pd.read_csv("olist_order_items_dataset.csv")
    order_payments = pd.read_csv("olist_order_payments_dataset.csv")
    products = pd.read_csv("olist_products_dataset.csv")
    return customers, orders, order_items, order_payments, products

customers, orders, order_items, order_payments, products = load_data()

# Sidebar
st.sidebar.title("Olist Dashboard")
option = st.sidebar.radio("Pilih Analisis:", ["Overview Data", "RFM Analysis", "Geospasial", "Performa Produk"])

# Overview Data
if option == "Overview Data":
    st.title("📊 Overview Data")
    st.write("Ringkasan dataset e-commerce Olist")
    st.write(f"Total Pelanggan: {customers.shape[0]}")
    st.write(f"Total Pesanan: {orders.shape[0]}")
    st.write(f"Total Produk: {products.shape[0]}")

    fig = px.histogram(orders, x="order_purchase_timestamp", nbins=50, title="Distribusi Waktu Pesanan")
    st.plotly_chart(fig)

# RFM Analysis
elif option == "RFM Analysis":
    st.title("📈 RFM Analysis")
    latest_date = orders["order_purchase_timestamp"].max()
    rfm = orders.groupby("customer_id").agg(
        recency=("order_purchase_timestamp", lambda x: (latest_date - x.max()).days),
        frequency=("order_id", "count"),
        monetary=("order_id", "count")
    ).reset_index()

    st.write("Distribusi Recency, Frequency, dan Monetary")
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].hist(rfm["recency"], bins=30, color="blue")
    axes[0].set_title("Recency")
    axes[1].hist(rfm["frequency"], bins=30, color="green")
    axes[1].set_title("Frequency")
    axes[2].hist(rfm["monetary"], bins=30, color="red")
    axes[2].set_title("Monetary")
    st.pyplot(fig)

# Geospasial
elif option == "Geospasial":
    st.title("🌍 Distribusi Geografis Pesanan")
    top_cities = customers["customer_city"].value_counts().head(10)
    fig = px.bar(x=top_cities.index, y=top_cities.values, labels={"x": "Kota", "y": "Jumlah Pesanan"}, title="Top 10 Kota dengan Transaksi Tertinggi")
    st.plotly_chart(fig)

# Performa Produk
elif option == "Performa Produk":
    st.title("🛍️ Performa Kategori Produk")
    category_sales = order_items.merge(products, on="product_id", how="left")
    top_categories = category_sales["product_category_name"].value_counts().head(10)
    fig = px.bar(x=top_categories.index, y=top_categories.values, labels={"x": "Kategori", "y": "Jumlah Terjual"}, title="Top 10 Kategori Produk")
    st.plotly_chart(fig)

import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="NeuralRetail Dashboard",
    layout="wide"
)

# Title
st.title("🛍️ NeuralRetail Intelligence Dashboard")

st.write("AI-Powered Retail Analytics & Predictive Intelligence Platform")

# Sidebar
st.sidebar.title("NeuralRetail Dashboard")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Sales Analysis",
        "Customer Insights",
        "Forecasting",
        "Inventory"
    ]
)


st.sidebar.markdown("---")

st.sidebar.info(
    "NeuralRetail AI Dashboard\n\nBuilt using Streamlit, Machine Learning & Retail Analytics"
)


# Load Data
retail = pd.read_csv("cleaned_retail_data.csv")

rfm = pd.read_csv("customer_churn_analysis.csv")

forecast = pd.read_csv("sales_forecast.csv")

inventory = pd.read_csv("inventory_analysis.csv")

# KPIs
total_revenue = retail['TotalPrice'].sum()

total_orders = retail['Invoice'].nunique()

total_customers = retail['Customer ID'].nunique()

total_products = retail['Description'].nunique()

# =========================
# Monthly Revenue Trend
# =========================

retail['InvoiceDate'] = pd.to_datetime(retail['InvoiceDate'])

retail['YearMonth'] = retail['InvoiceDate'].dt.to_period('M').astype(str)

monthly_sales = retail.groupby('YearMonth')['TotalPrice'].sum().reset_index()

fig1 = px.line(
    monthly_sales,
    x='YearMonth',
    y='TotalPrice',
    title='Monthly Revenue Trend'
)

# =========================
# Top Selling Products
# =========================

top_products = retail.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)

top_products = top_products.reset_index()

fig2 = px.bar(
    top_products,
    x='Description',
    y='Quantity',
    title='Top 10 Selling Products'
)

# =========================
# Customer Segments
# =========================

segment_counts = rfm['Cluster_Label'].value_counts().reset_index()

segment_counts.columns = ['Segment', 'Count']

fig3 = px.pie(
    segment_counts,
    names='Segment',
    values='Count',
    title='Customer Segmentation'
)

# =========================
# Forecast Chart
# =========================

forecast_chart = forecast[['ds', 'yhat']].tail(12)

fig4 = px.line(
    forecast_chart,
    x='ds',
    y='yhat',
    title='Sales Forecast Prediction'
)

# =========================
# Inventory Chart
# =========================

top_inventory = inventory.sort_values(
    by='Total_Quantity_Sold',
    ascending=False
).head(10)

fig5 = px.bar(
    top_inventory,
    x=top_inventory.index,
    y='Total_Quantity_Sold',
    title='High Demand Products'
)

# =========================
# Churn Chart
# =========================

churn_counts = rfm['Churn'].value_counts().reset_index()

churn_counts.columns = ['Churn', 'Count']

fig6 = px.pie(
    churn_counts,
    names='Churn',
    values='Count',
    title='Customer Churn Distribution'
)

# =========================
# PAGE NAVIGATION
# =========================

# OVERVIEW PAGE
if page == "Overview":

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Revenue", f"${total_revenue:,.0f}")

    col2.metric("Total Orders", total_orders)

    col3.metric("Total Customers", total_customers)

    col4.metric("Total Products", total_products)

    st.subheader("📈 Monthly Revenue Trend")

    st.plotly_chart(fig1, use_container_width=True)

# SALES ANALYSIS PAGE
elif page == "Sales Analysis":
    st.subheader("🏆 Top Selling Products")

    st.plotly_chart(fig2, use_container_width=True)

    

# CUSTOMER INSIGHTS PAGE
elif page == "Customer Insights":
    st.subheader("👥 Customer Segmentation")

    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("⚠️ Customer Churn Analysis")

    st.plotly_chart(fig6, use_container_width=True)

    

# FORECASTING PAGE
elif page == "Forecasting":
    st.subheader("🔮 Sales Forecasting")

    st.plotly_chart(fig4, use_container_width=True)

    

# INVENTORY PAGE
elif page == "Inventory":

    st.subheader("📦 Inventory Optimization")

    st.plotly_chart(fig5, use_container_width=True)


# footer
st.markdown("---")

st.caption("Developed by Snehaa Gupta 🚀")    
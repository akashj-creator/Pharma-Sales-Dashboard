import streamlit as st
import plotly.express as px
import pandas as pd
import data_processor as dp

st.set_page_config(page_title="Sales Deep Dive", page_icon="🔍", layout="wide")

@st.cache_data
def get_data():
    raw_data = dp.load_data()
    if raw_data:
        return dp.process_data(raw_data)
    return None

data = get_data()
if not data:
    st.stop()

sales_df = data['sales_enriched']

st.title("🔍 Sales Deep Dive")

# --- Filters ---
st.sidebar.header("Filters")
selected_region = st.sidebar.selectbox("Region", ["All"] + sorted(sales_df['Region'].unique().tolist()))

if selected_region != "All":
    sales_df = sales_df[sales_df['Region'] == selected_region]

# --- Therapeutic Area Analysis ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales by Therapeutic Class")
    area_sales = sales_df.groupby('TherapeuticClass')['InvoiceAmount'].sum().reset_index()
    fig_donut = px.pie(area_sales, values='InvoiceAmount', names='TherapeuticClass', hole=0.4, title="Revenue Share by Class")
    st.plotly_chart(fig_donut, use_container_width=True)

with col2:
    st.subheader("Payment Method Distribution")
    pay_sales = sales_df.groupby('PaymentMethod')['InvoiceAmount'].sum().reset_index()
    fig_pie = px.pie(pay_sales, values='InvoiceAmount', names='PaymentMethod', title="Revenue by Payment Method")
    st.plotly_chart(fig_pie, use_container_width=True)

# --- Distributor Performance ---
st.subheader("Distributor Performance")
dist_perf = sales_df.groupby(['DistributorName', 'City'])[['InvoiceAmount', 'UnitsSold']].sum().reset_index()
dist_perf = dist_perf.sort_values('InvoiceAmount', ascending=False)

st.dataframe(dist_perf.style.format({"InvoiceAmount": "${:,.2f}", "UnitsSold": "{:,.0f}"}), use_container_width=True)

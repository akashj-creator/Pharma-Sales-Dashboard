import streamlit as st
import plotly.express as px
import pandas as pd
import data_processor as dp

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

# --- Load Data ---
@st.cache_data
def get_data():
    raw_data = dp.load_data()
    if raw_data:
        return dp.process_data(raw_data)
    return None

data = get_data()
if not data:
    st.error("Data not found.")
    st.stop()

sales_df = data['sales_enriched']

# --- Sidebar Filters ---
st.sidebar.header("Filters")
# Date Range
min_date = sales_df['Date'].min()
max_date = sales_df['Date'].max()

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# Region Filter
regions = sorted(sales_df['Region'].unique().tolist())
selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)

# --- Filter Data ---
mask = (sales_df['Date'] >= pd.to_datetime(start_date)) & \
       (sales_df['Date'] <= pd.to_datetime(end_date)) & \
       (sales_df['Region'].isin(selected_regions))

filtered_df = sales_df[mask]

# --- KPIs ---
st.title("📊 Executive Overview")

col1, col2, col3, col4 = st.columns(4)
with col1:
    total_rev = filtered_df['InvoiceAmount'].sum()
    st.metric("Total Revenue", f"${total_rev:,.2f}")
with col2:
    total_units = filtered_df['UnitsSold'].sum()
    st.metric("Units Sold", f"{total_units:,.0f}")
with col3:
    avg_discount = filtered_df['DiscountPercent'].mean()
    st.metric("Avg Discount", f"{avg_discount:.2f}%")
with col4:
    num_txns = len(filtered_df)
    st.metric("Transactions", f"{num_txns:,}")

st.markdown("---")

# --- Charts ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Sales Trend Over Time")
    # Aggregate by Month
    sales_trend = filtered_df.groupby(filtered_df['Date'].dt.to_period('M'))['InvoiceAmount'].sum().reset_index()
    sales_trend['Date'] = sales_trend['Date'].dt.to_timestamp()
    
    fig_trend = px.line(sales_trend, x='Date', y='InvoiceAmount', markers=True, title="Monthly Revenue Trend")
    st.plotly_chart(fig_trend, use_container_width=True)

with col_right:
    st.subheader("Revenue by Region")
    region_sales = filtered_df.groupby('Region')['InvoiceAmount'].sum().reset_index()
    fig_region = px.bar(region_sales, x='Region', y='InvoiceAmount', color='Region', title="Total Revenue by Region")
    st.plotly_chart(fig_region, use_container_width=True)

# --- Top Products ---
st.subheader("Top 5 Products by Revenue")
top_products = filtered_df.groupby('ProductName')['InvoiceAmount'].sum().nlargest(5).reset_index()
fig_prod = px.bar(top_products, x='InvoiceAmount', y='ProductName', orientation='h', title="Top 5 Products")
st.plotly_chart(fig_prod, use_container_width=True)

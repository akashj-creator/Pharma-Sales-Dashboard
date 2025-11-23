import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import data_processor as dp

st.set_page_config(page_title="Inventory & Targets", page_icon="📦", layout="wide")

@st.cache_data
def get_data():
    raw_data = dp.load_data()
    if raw_data:
        return dp.process_data(raw_data)
    return None

data = get_data()
if not data:
    st.stop()

inventory_df = data['inventory_enriched']
targets_df = data['targets']

st.title("📦 Inventory & Targets")

# --- Inventory Section ---
st.header("Inventory Status")

# Low Stock Alert
low_stock = inventory_df[inventory_df['StockLevel'] < inventory_df['ReorderLevel']]

if not low_stock.empty:
    st.error(f"⚠️ Alert: {len(low_stock)} products are below reorder level!")
    st.dataframe(low_stock[['ProductName', 'StockLevel', 'ReorderLevel', 'TherapeuticClass']], use_container_width=True)
else:
    st.success("✅ All stock levels are healthy.")

# Stock Distribution
fig_stock = px.histogram(inventory_df, x='StockLevel', nbins=20, title="Stock Level Distribution")
st.plotly_chart(fig_stock, use_container_width=True)

st.markdown("---")

# --- Targets Section ---
st.header("Regional Target Achievement")

# Calculate Achievement
# Note: In a real scenario, we would aggregate actual sales by Region/Month and join with targets.
# For this demo, we'll use the pre-calculated 'AchievementPercent' in the targets file if available,
# or visualize the raw target data.

if 'AchievementPercent' in targets_df.columns:
    # Average Achievement by Region
    avg_ach = targets_df.groupby('Region')['AchievementPercent'].mean().reset_index()
    
    fig_bar = px.bar(avg_ach, x='Region', y='AchievementPercent', color='AchievementPercent',
                     title="Average Target Achievement % by Region",
                     color_continuous_scale='RdYlGn')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Detailed Table
    st.subheader("Detailed Target Data")
    st.dataframe(targets_df, use_container_width=True)

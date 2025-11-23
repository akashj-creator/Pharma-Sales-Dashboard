import streamlit as st
import data_processor as dp

# --- Page Config ---
st.set_page_config(
    page_title="Pharma Analytics Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Load Data ---
@st.cache_data
def get_data():
    raw_data = dp.load_data()
    if raw_data:
        return dp.process_data(raw_data)
    return None

data = get_data()

if not data:
    st.error("Failed to load data. Please check if the CSV files are in the 'data' folder.")
    st.stop()

# --- Sidebar ---
st.sidebar.title("💊 Pharma Analytics")
st.sidebar.info("Navigate using the sidebar menu above.")

# --- Main Content ---
st.title("Welcome to Pharma Analytics Dashboard")
st.markdown("""
This dashboard provides a comprehensive view of your pharmaceutical sales, inventory, and target performance.

### 👈 Select a page from the sidebar to get started:

- **Overview**: High-level KPIs and sales trends.
- **Sales Deep Dive**: Detailed analysis by distributor, product, and region.
- **Inventory & Targets**: Stock levels and regional performance against targets.
""")

# --- Quick Stats Preview ---
col1, col2, col3 = st.columns(3)
with col1:
    total_sales = data['sales_enriched']['InvoiceAmount'].sum()
    st.metric("Total Revenue (All Time)", f"${total_sales:,.2f}")
with col2:
    total_units = data['sales_enriched']['UnitsSold'].sum()
    st.metric("Total Units Sold", f"{total_units:,.0f}")
with col3:
    active_distributors = data['sales_enriched']['DistributorID'].nunique()
    st.metric("Active Distributors", active_distributors)

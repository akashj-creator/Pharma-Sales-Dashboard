# Pharma Sales Analytics Dashboard

A comprehensive interactive dashboard for pharmaceutical sales analysis, built with **Streamlit** and **Python**.

## Features

- **Executive Overview**: High-level KPIs (Revenue, Units, Discount) and sales trends.
- **Sales Deep Dive**: Detailed analysis by Distributor, Therapeutic Area, and Payment Method.
- **Inventory & Targets**: Stock level alerts and regional target achievement tracking.

## Setup & Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Dashboard**:
    ```bash
    streamlit run streamlit_app.py
    ```

## Data Source
The dashboard uses CSV files located in the `data/` directory:
- `Pharma_Sales.csv`
- `Pharma_Product_Master.csv`
- `Pharma_Distributor_Master.csv`
- `Pharma_Inventory.csv`
- `Pharma_Region_Targets.csv`

## Project Structure
- `streamlit_app.py`: Main application entry point.
- `pages/`: Individual dashboard pages.
- `data_processor.py`: Data loading and cleaning logic.

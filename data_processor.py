import pandas as pd
import os

DATA_DIR = "data"

def load_data():
    """
    Loads all pharma datasets from the data directory.
    Returns a dictionary of DataFrames.
    """
    files = {
        "distributors": "Pharma_Distributor_Master.csv",
        "inventory": "Pharma_Inventory.csv",
        "products": "Pharma_Product_Master.csv",
        "targets": "Pharma_Region_Targets.csv",
        "sales": "Pharma_Sales.csv"
    }
    
    dfs = {}
    for key, filename in files.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            dfs[key] = pd.read_csv(path)
        else:
            print(f"Warning: {filename} not found in {DATA_DIR}")
            return None

    return dfs

def process_data(dfs):
    """
    Cleans and merges the datasets into a unified model.
    """
    sales = dfs["sales"].copy()
    products = dfs["products"].copy()
    distributors = dfs["distributors"].copy()
    targets = dfs["targets"].copy()
    inventory = dfs["inventory"].copy()

    # --- 1. Clean Sales Data ---
    # Convert Date to datetime
    sales['Date'] = pd.to_datetime(sales['Date'])
    sales['Month'] = sales['Date'].dt.to_period('M')
    sales['Year'] = sales['Date'].dt.year
    
    # Ensure numeric types
    sales['InvoiceAmount'] = pd.to_numeric(sales['InvoiceAmount'], errors='coerce').fillna(0)
    sales['UnitsSold'] = pd.to_numeric(sales['UnitsSold'], errors='coerce').fillna(0)

    # --- 2. Merge Sales with Dimensions ---
    # Merge with Product Master
    # Common column: ProductID
    sales_enriched = sales.merge(products, on='ProductID', how='left')
    
    # Merge with Distributor Master
    # Common column: DistributorID
    sales_enriched = sales_enriched.merge(distributors, on='DistributorID', how='left')

    # --- 3. Clean Targets ---
    # Targets are at Region-Quarter level. 
    # We might want to map Months to Quarters for comparison.
    
    # --- 4. Clean Inventory ---
    # Ensure numeric
    inventory['StockLevel'] = pd.to_numeric(inventory['StockLevel'], errors='coerce').fillna(0)
    inventory['ReorderLevel'] = pd.to_numeric(inventory['ReorderLevel'], errors='coerce').fillna(0)
    
    # Merge Inventory with Product Name for better display
    inventory_enriched = inventory.merge(products[['ProductID', 'ProductName', 'TherapeuticClass']], on='ProductID', how='left')

    return {
        "sales_enriched": sales_enriched,
        "targets": targets,
        "inventory_enriched": inventory_enriched,
        "products": products,
        "distributors": distributors
    }

if __name__ == "__main__":
    # Test the loading
    print("Loading data...")
    dfs = load_data()
    if dfs:
        print("Data loaded successfully.")
        processed = process_data(dfs)
        print("Data processed successfully.")
        print(f"Enriched Sales Shape: {processed['sales_enriched'].shape}")
        print(f"Sample Sales Record:\n{processed['sales_enriched'].iloc[0]}")
    else:
        print("Failed to load data.")

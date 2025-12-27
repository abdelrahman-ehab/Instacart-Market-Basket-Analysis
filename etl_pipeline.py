import pandas as pd
from sqlalchemy import create_engine
import time

# --- CONFIGURATION ---
# Update this string with your actual Postgres credentials
DB_CONN = "postgresql://postgres:newpassword@localhost:5432/Instacart"
DATA_DIR = "data/" 

def load_data_to_postgres():
    engine = create_engine(DB_CONN)
    
    # 1. Load Dimensions (Small tables)
    files = {
        'aisles': 'aisles.csv',
        'departments': 'departments.csv', 
        'products': 'products.csv',
        'orders': 'orders.csv' # This is larger, but manageable
    }

    print("--- Starting ETL Process ---")

    for table_name, file_name in files.items():
        print(f"Processing {table_name}...")
        df = pd.read_csv(f"{DATA_DIR}{file_name}")
        
        # TRANSFORMATION: Handle NaN in 'days_since_prior_order' for new users (Set to 0 or -1)
        if table_name == 'orders':
            df['days_since_prior_order'] = df['days_since_prior_order'].fillna(0)
            
        # LOAD
        df.to_sql(table_name, engine, if_exists='append', index=False, chunksize=10000)
        print(f"Uploaded {len(df)} rows to {table_name}.")

    # 2. Load and Merge Transaction Data (The "Big" Transformation)
    print("Processing Order_Products (Merging Prior + Train)...")
    
    # Extract
    df_prior = pd.read_csv(f"{DATA_DIR}order_products__prior.csv")
    df_train = pd.read_csv(f"{DATA_DIR}order_products__train.csv")
    
    # Transform: Union them together
    df_transactions = pd.concat([df_prior, df_train])
    
    print(f"Total Transactions to load: {len(df_transactions)}")
    
    # Load (Using chunksize is critical for millions of rows to avoid memory crash)
    start_time = time.time()
    df_transactions.to_sql('order_products', engine, if_exists='append', index=False, chunksize=10000)
    
    print(f"--- ETL Finished in {round(time.time() - start_time, 2)} seconds ---")

if __name__ == "__main__":
    load_data_to_postgres()
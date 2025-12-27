import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules
from sqlalchemy import create_engine
import os

# --- 1. CONFIGURATION ---
DB_CONN = "postgresql://postgres:newpassword@localhost:5432/Instacart"
engine = create_engine(DB_CONN)

# We only analyze the Top 100 products to prevent memory crashes (Vital Few)
LIMIT_PRODUCTS = 100 

def run_market_basket():
    print("--- Phase 3: Market Basket Analysis Started ---")
    
    # --- 2. DATA EXTRACTION (SQL) ---
    print(f"Fetching transactions for the Top {LIMIT_PRODUCTS} products...")
    
    query = f"""
    WITH TopProducts AS (
        SELECT product_id 
        FROM order_products 
        GROUP BY product_id 
        ORDER BY count(*) DESC 
        LIMIT {LIMIT_PRODUCTS}
    )
    SELECT 
        op.order_id, 
        p.product_name
    FROM order_products op
    JOIN products p ON op.product_id = p.product_id
    INNER JOIN TopProducts tp ON op.product_id = tp.product_id
    -- Sample size: Grab 50,000 orders to keep it fast for testing
    WHERE op.order_id IN (SELECT order_id FROM orders LIMIT 50000);
    """
    
    df = pd.read_sql(query, engine)
    print(f"Data Loaded: {len(df)} rows. Transforming to Transaction Matrix...")

    # --- 3. DATA TRANSFORMATION (One-Hot Encoding) ---
    # We need a matrix where Index = Order_ID, Columns = Product_Name, Value = 1 if bought
    basket = (df.groupby(['order_id', 'product_name'])['product_name']
              .count().unstack().reset_index().fillna(0)
              .set_index('order_id'))

    # Convert counts to Booleans (1s and 0s) 
    basket = basket.map(lambda x: True if x > 0 else False)
    
    print(f"Matrix Ready. Shape: {basket.shape}")

    #  4. THE ALGORITHM (FP-GROWTH) ---
    print("Running FP-Growth Algorithm...")
    
    # min_support=0.01 means "This combo must appear in at least 1% of all orders"
    frequent_itemsets = fpgrowth(basket, min_support=0.01, use_colnames=True)
    
    print(f"Found {len(frequent_itemsets)} frequent item patterns.")

    # 5. GENERATING RULES ---
    print("Generating Association Rules...")
    
    #  We only want rules better than random chance
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.2)
    
    # Sorting by 'Lift' to see the strongest correlations first
    rules = rules.sort_values(by=['lift'], ascending=False)
    
    # --- 6. OUTPUT ---
    # Select clean columns for display
    output = rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
    
    print("\n--- TOP 10 RULES FOUND ---")
    print(output.head(10))
    
    # Save to CSV for Power BI later
    output.to_csv('market_basket_rules.csv', index=False)
    print("\nRules saved to 'market_basket_rules.csv'")

if __name__ == "__main__":
    run_market_basket()
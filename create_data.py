import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# Setup
os.makedirs("raw_data", exist_ok=True)
np.random.seed(42)  # For reproducible messiness

# --- 1. Generate Product Master (The Clean List) ---
products = {
    'product_id': range(101, 151),  # IDs 101 to 150
    'product_name': [
        'Angus Beef', 'Local Chicken', 'Salmon Fillet', 'Tiger Prawns', 'Milk 1L',
        'Cheddar Cheese', 'Butter Salted', 'Eggs (Tray)', 'Rice 10kg', 'Cooking Oil 5kg',
        'Sugar 1kg', 'Flour 1kg', 'Soy Sauce', 'Chili Sauce', 'Oyster Sauce',
        'Garlic (kg)', 'Onion (kg)', 'Potato (kg)', 'Carrot (kg)', 'Broccoli (kg)',
        'Apple Fuji', 'Orange Navel', 'Grapes Black', 'Watermelon', 'Papaya',
        'Coffee Beans', 'Tea Bags', 'Milo 1kg', 'Cola 1.5L', 'Mineral Water',
        'Dish Soap', 'Laundry Det', 'Toilet Paper', 'Kitchen Towel', 'Trash Bags',
        'Sponge', 'Bleach', 'Floor Cleaner', 'Glass Cleaner', 'Air Freshener',
        'Dog Food', 'Cat Food', 'Bird Seed', 'Fish Food', 'Pet Shampoo',
        'Notebook', 'Pen Blue', 'Pencil 2B', 'A4 Paper', 'Stapler'
    ],
    'category': (
            ['Fresh Food'] * 5 + ['Dairy'] * 3 + ['Groceries'] * 7 + ['Vegetables'] * 5 +
            ['Fruits'] * 5 + ['Beverages'] * 5 + ['Household'] * 10 + ['Pet'] * 5 + ['Stationery'] * 5
    ),
    'price': np.round(np.random.uniform(2.50, 150.00, 50), 2),
    'safety_stock': np.random.randint(10, 50, 50)
}
df_products = pd.DataFrame(products)

# Save Master Data
df_products.to_csv("raw_data/products_master.csv", index=False)
print("Generated raw_data/products_master.csv")

# --- 2. Generate Messy Transactions (Sales & Restocks) ---
start_date = datetime(2026, 1, 1)
dates = [start_date + timedelta(days=x) for x in range(90)]  # 3 months

transactions = []

for date in dates:
    # Randomly select 15-20 products to transact each day
    daily_products = random.sample(list(products['product_id']), k=random.randint(15, 25))

    for pid in daily_products:
        # 80% chance of Sale (Negative), 20% chance of Restock (Positive)
        if random.random() > 0.2:
            txn_type = "SALE"
            qty = -np.random.randint(1, 10)  # Sales remove stock
        else:
            txn_type = "RESTOCK"
            qty = np.random.randint(20, 100)  # Restocks add stock

        transactions.append([date, pid, qty, txn_type])

# Create DataFrame
df_txn = pd.DataFrame(transactions, columns=['date', 'product_id', 'qty', 'type'])

# --- 3. INJECT THE MESS (The "Real World" Problems) ---

# Mess 1: Formatting issues in dates (String vs Date object)
# We will leave dates clean for now to avoid breaking SQL load immediately,
# but let's add some NULL quantities.
for _ in range(20):
    idx = random.randint(0, len(df_txn) - 1)
    df_txn.at[idx, 'qty'] = np.nan  # Missing quantity

# Mess 2: Orphan Records (Selling a product that doesn't exist)
new_row = {'date': start_date, 'product_id': 999, 'qty': -5, 'type': 'SALE'}
df_txn = pd.concat([df_txn, pd.DataFrame([new_row])], ignore_index=True)

# Mess 3: Duplicates (Accidental double scan)
duplicate_rows = df_txn.sample(n=30)
df_txn = pd.concat([df_txn, duplicate_rows], ignore_index=True)

# Save Transaction Data
df_txn.to_csv("raw_data/daily_transactions.csv", index=False)
print(f"✅ Generated raw_data/daily_transactions.csv with {len(df_txn)} rows")

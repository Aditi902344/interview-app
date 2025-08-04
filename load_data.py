import sqlite3
import pandas as pd

# Step 1: Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('ecommerce.db')  # Database file will be created in your project folder
cursor = conn.cursor()

# Step 2: Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    phone TEXT
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    product TEXT,
    amount REAL,
    order_date TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Step 3: Load CSV files into pandas
users_df = pd.read_csv('users.csv')
orders_df = pd.read_csv('orders.csv')

# Step 4: Insert data into tables
users_df.to_sql('users', conn, if_exists='replace', index=False)
orders_df.to_sql('orders', conn, if_exists='replace', index=False)

# Step 5: Verify by querying
print("Users:")
for row in cursor.execute('SELECT * FROM users LIMIT 5'):
    print(row)

print("\nOrders:")
for row in cursor.execute('SELECT * FROM orders LIMIT 5'):
    print(row)

# Step 6: Close connection
conn.close()

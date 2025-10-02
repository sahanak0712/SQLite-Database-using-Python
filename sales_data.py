#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import os

DB_FILE = "sales_data.db"   # The DB file will be created in the current folder


# In[2]:


sql_create = """
DROP TABLE IF EXISTS sales;

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date   TEXT NOT NULL,   -- dd-mm-yyyy
    product TEXT NOT NULL,
    store   TEXT NOT NULL,
    region  TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price    REAL NOT NULL
);
"""

with sqlite3.connect(DB_FILE) as conn:
    conn.executescript(sql_create)

print("Table `sales` created in", os.path.abspath(DB_FILE))


# In[3]:


sql_insert = """
INSERT INTO sales (date, product, store, region, quantity, price) VALUES
('01-09-2025','Product_001','Store_A','North',  5,  53.00),
('01-09-2025','Product_003','Store_D','East',   2, 128.50),
('02-09-2025','Product_009','Store_B','North',  2, 127.00),
('03-09-2025','Product_007','Store_A','South',  4,  45.00),
('04-09-2025','Product_010','Store_C','West',   1,  56.50),
('05-09-2025','Product_004','Store_C','North',  3, 116.50),
('06-09-2025','Product_008','Store_E','East',   6,  64.50),
('07-09-2025','Product_001','Store_B','South',  3,  53.00),
('08-09-2025','Product_003','Store_E','North', 10, 128.50),
('09-09-2025','Product_006','Store_D','West',   4, 113.50),
('10-09-2025','Product_009','Store_B','North', 10, 127.00),
('11-09-2025','Product_003','Store_D','North',  2, 128.50),
('12-09-2025','Product_002','Store_A','East',   7,  15.50),
('13-09-2025','Product_005','Store_C','South',  4,  65.50),
('14-09-2025','Product_007','Store_A','South',  2,  45.00),
('15-09-2025','Product_010','Store_A','West',   3,  56.50),
('16-09-2025','Product_004','Store_B','North',  9, 116.50),
('17-09-2025','Product_008','Store_E','West',   5,  64.50),
('18-09-2025','Product_001','Store_E','North',  2,  53.00),
('19-09-2025','Product_006','Store_C','East',   6, 113.50);
"""

with sqlite3.connect(DB_FILE) as conn:
    conn.executescript(sql_insert)
    conn.commit()

print("Inserted 20 rows.")


# In[4]:


with sqlite3.connect(DB_FILE) as conn:
    df_preview = pd.read_sql_query("SELECT * FROM sales", conn)

df_preview


# In[5]:


with sqlite3.connect(DB_FILE) as conn:
    df_preview = pd.read_sql_query("SELECT * FROM sales ORDER BY id LIMIT 10;", conn)

df_preview


# In[8]:


# Per-product totals (quantity and revenue)
per_product_sql = """
SELECT
  product,
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
"""

with sqlite3.connect(DB_FILE) as conn:
    df_products = pd.read_sql_query(per_product_sql, conn)
    
print("=== Per-Product Summary ===")
print(df_products.to_string(index=False))


# In[9]:


# Overall totals
overall_sql = """
SELECT
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales;
"""
with sqlite3.connect(DB_FILE) as conn:
    df_overall  = pd.read_sql_query(overall_sql, conn)
print("\n=== Overall Totals ===")
print(df_overall.to_string(index=False))
    


# In[10]:


import matplotlib.pyplot as plt

plt.figure()
plt.bar(df_products["product"], df_products["revenue"])
plt.title("Revenue by Product (20-row demo)")
plt.xlabel("Product")
plt.ylabel("Revenue")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()


# In[12]:


# Per-Store Totals (quantity + revenue)
store_sql = """
SELECT
  store,
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY store
ORDER BY revenue DESC;
"""

with sqlite3.connect(DB_FILE) as conn:
    df_store = pd.read_sql_query(store_sql, conn)

print("=== Per-Store Summary ===")
print(df_store.to_string(index=False))
df_store


# In[13]:


# Per-Region Totals (quantity + revenue)
region_sql = """
SELECT
  region,
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;
"""

with sqlite3.connect(DB_FILE) as conn:
    df_region = pd.read_sql_query(region_sql, conn)

print("=== Per-Region Summary ===")
print(df_region.to_string(index=False))
df_region


# In[14]:


# Revenue by Region (bar chart)
import matplotlib.pyplot as plt

plt.figure()
plt.bar(df_region["region"], df_region["revenue"])
plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()


# In[21]:


# daily query + line chart
daily_sql = """
SELECT date, SUM(quantity * price) AS revenue
FROM sales
GROUP BY date;
"""
with sqlite3.connect(DB_FILE) as conn:
    df_daily = pd.read_sql_query(daily_sql, conn)

# parse dd-mm-yyyy for correct chronological plotting
df_daily["date_parsed"] = pd.to_datetime(df_daily["date"], dayfirst=True)
df_daily = df_daily.sort_values("date_parsed")

plt.figure()
plt.plot(df_daily["date_parsed"], df_daily["revenue"])
plt.title("Daily Revenue")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.tight_layout()


import matplotlib.dates as mdates
ax = plt.gca()
ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
plt.gcf().autofmt_xdate(rotation=45, ha='right')


# In[ ]:





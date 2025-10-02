# SQLite-Database-using-Python
 Using SQL inside Python to pull simple sales info (like total quantity sold, total revenue), and  display it using basic print statements and a simple bar chart

# Basic Sales Summary (SQLite + Python)

A small, reproducible project that:
- Creates a local **SQLite** database (`sales_data.db`)
- Inserts a demo **sales** table (date in `dd-mm-yyyy`, store, region, product, quantity, price)
- Runs simple **SQL** summaries from Python (`sqlite3` + `pandas`)
- Saves **PNG charts** to the `figures/` folder using **matplotlib** (no styling required)

## What's inside
```
.
├─ sales_data.py      # Creates DB, seeds demo data, runs SQL, saves charts as PNGs
├─ sales_data.db      # Auto-generated SQLite database (created on first run)
├─ figures/           # Auto-generated chart images
│  ├─ revenue_by_product.png
│  ├─ revenue_by_region.png
│  └─ daily_revenue.png
└─ README.md          # This file
```

## Quickstart

> Python 3.10+ recommended

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install pandas matplotlib
python sales_data.py
```

On first run, you'll see:
1. `sales_data.db` created with a fresh `sales` table
2. 20 demo rows inserted (easily extend to 50 by adding INSERTs in the script)
3. SQL summaries printed in the console
4. Charts saved to `figures/`:
   - `revenue_by_product.png`
   - `revenue_by_region.png`
   - `daily_revenue.png`

## Table schema (`sales`)

- `id` INTEGER PRIMARY KEY
- `date` TEXT (format `dd-mm-yyyy`)
- `product` TEXT
- `store` TEXT
- `region` TEXT
- `quantity` INTEGER
- `price` REAL

## Example SQL used

**Per-product revenue**
```sql
SELECT
  product,
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY product
ORDER BY revenue DESC;
```

**Per-region revenue**
```sql
SELECT
  region,
  SUM(quantity) AS total_qty,
  ROUND(SUM(quantity * price), 2) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;
```

**Daily revenue**
```sql
SELECT date, SUM(quantity * price) AS revenue
FROM sales
GROUP BY date
ORDER BY date;
```

## Charts & readable dates

The script converts `dd-mm-yyyy` into datetimes (`dayfirst=True`), uses an automatic date locator and a concise date formatter, rotates labels, and applies `tight_layout()` for readability. Each chart is saved as a separate PNG under `figures/`.

## Extend the demo data

To scale from 20 rows to ~50, add more `INSERT` statements in `sales_data.py` within the `seed_data` list (keep the same format). Re-run the script to regenerate summaries and charts.

## Why this repo?

- Clean, minimal example of running **SQL inside Python** for quick analysis
- Demonstrates a common pattern: **SQLite + pandas + matplotlib**
- Produces portable **artifacts** (DB + PNG charts) that you can drop into reports



#9. Load final Cleaned and merge Dataframe 
import pandas as pd
import sqlite3
import os

print("TASK 4: DATA LOADING INTO SQLITE")

final_df = pd.read_csv("output/final_cleaned_data.csv")

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("output/retail_sales.db")

final_df.to_sql("retail_sales", conn, if_exists="replace", index=False)

print("\nData loaded into SQLite table: retail_sales")


#10.Top 3 Selling products 
query = """
SELECT 
    product_name,
    SUM(quantity) AS total_quantity_sold
FROM retail_sales
WHERE product_name IS NOT NULL
GROUP BY product_name
ORDER BY total_quantity_sold DESC
LIMIT 3;
"""

top_products = pd.read_sql_query(query, conn)

print("\nTop 3 Best Selling Products:")
print(top_products)

top_products.to_csv("output/top_products_report.csv", index=False)

conn.close()

print("\nTop products report saved as output/top_products_report.csv")

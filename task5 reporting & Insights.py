## 11. Total Revenue of per store per day 
import pandas as pd
import sqlite3

print("TASK 5: REPORTING AND INSIGHTS")

final_df = pd.read_csv("output/final_cleaned_data.csv")

conn = sqlite3.connect("output/retail_sales.db")

query = """
SELECT 
    store_name,
    sale_date,
    SUM(total_revenue) AS daily_revenue
FROM retail_sales
WHERE store_name IS NOT NULL
GROUP BY store_name, sale_date
ORDER BY sale_date;
"""

store_report = pd.read_sql_query(query, conn)

print("\nTotal Revenue Per Store Per Day:")
print(store_report)

##12. Summary Report of Total Transactions, total Revenue , Top selling city & top selling product 

store_report.to_csv("output/store_daily_revenue_report.csv", index=False)

conn.close()

valid_data = final_df.dropna(subset=["product_name", "store_name"])

total_transactions = valid_data.shape[0]
total_revenue = valid_data["total_revenue"].sum()

top_city = valid_data.groupby("city")["total_revenue"].sum().idxmax()
top_product = valid_data.groupby("product_name")["quantity"].sum().idxmax()

print("\nSummary Report")
print("Total Number of Transactions:", total_transactions)
print("Total Revenue:", total_revenue)
print("Top Selling City:", top_city)
print("Top Selling Product:", top_product)

print("\nStore daily revenue report saved as output/store_daily_revenue_report.csv")
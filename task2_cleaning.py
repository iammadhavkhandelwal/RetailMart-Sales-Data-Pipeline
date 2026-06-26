import pandas as pd
import os

sales_df = pd.read_csv("data/sales_data.csv")

print("TASK 2: DATA CLEANING")

duplicate_rows = sales_df.duplicated().sum()
print("\nDuplicate rows found:", duplicate_rows)

sales_df = sales_df.drop_duplicates().copy()
print("Duplicate rows removed:", duplicate_rows)

sales_df["quantity"] = sales_df["quantity"].fillna(0)

before_rows = sales_df.shape[0]
sales_df = sales_df.dropna(subset=["amount"]).copy()
after_rows = sales_df.shape[0]

print("Rows removed where amount is NULL:", before_rows - after_rows)

sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], errors="coerce")
sales_df["amount"] = sales_df["amount"].astype(float)
sales_df["quantity"] = sales_df["quantity"].astype(int)

print("\nCleaned Sales Data Shape:", sales_df.shape)
print(sales_df.head())

print("\nData Types After Cleaning:")
print(sales_df.dtypes)

os.makedirs("output", exist_ok=True)
sales_df.to_csv("output/cleaned_sales_data.csv", index=False)

print("\nCleaned sales data saved as output/cleaned_sales_data.csv")
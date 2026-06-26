import pandas as pd
import numpy as np
import os

sales_df = pd.read_csv("output/cleaned_sales_data.csv")
products_df = pd.read_csv("data/products.csv")
stores_df = pd.read_csv("data/stores.csv")

print("TASK 3: DATA TRANSFORMATION")

sales_df["product_id"] = sales_df["product_id"].astype(str).str.strip()
products_df["product_id"] = products_df["product_id"].astype(str).str.strip()

sales_df["store_id"] = sales_df["store_id"].astype(str).str.strip()
stores_df["store_id"] = stores_df["store_id"].astype(str).str.strip()

final_df = pd.merge(sales_df, products_df, on="product_id", how="left")
final_df = pd.merge(final_df, stores_df, on="store_id", how="left")

#Total Revenue= quantity*Price 
final_df["total_revenue"] = np.multiply(final_df["quantity"], final_df["price"])

print("\nFinal Merged DataFrame:")
print(final_df)

print("\nRevenue Summary:")
print("Mean Revenue:", np.nanmean(final_df["total_revenue"]))
print("Maximum Revenue:", np.nanmax(final_df["total_revenue"]))
print("Minimum Revenue:", np.nanmin(final_df["total_revenue"]))

city_revenue = final_df.groupby("city")["total_revenue"].sum()
city_revenue = city_revenue.sort_values(ascending=False)

print("\nTotal Revenue Per City:")
print(city_revenue)

wrong_products = final_df[final_df["product_name"].isnull()]
wrong_stores = final_df[final_df["store_name"].isnull()]

print("\nIncorrect Product Records:", wrong_products.shape[0])
print("Incorrect Store Records:", wrong_stores.shape[0])

if not wrong_products.empty:
    print("\nRows with incorrect product id:")
    print(wrong_products[["sale_id", "product_id", "quantity", "amount"]])

if not wrong_stores.empty:
    print("\nRows with incorrect store id:")
    print(wrong_stores[["sale_id", "store_id", "quantity", "amount"]])

os.makedirs("output", exist_ok=True)
final_df.to_csv("output/final_cleaned_data.csv", index=False)
city_revenue.to_csv("output/city_revenue_report.csv")

print("\nFinal cleaned data saved as output/final_cleaned_data.csv")
print("City revenue report saved as output/city_revenue_report.csv")
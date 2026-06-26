import pandas as pd
import numpy as np
import sqlite3
import os

sales_file = "data/sales_data.csv"
products_file = "data/products.csv"
stores_file = "data/stores.csv"


def run_pipeline():
    try:
        print("FINAL PIPELINE")

        sales_df = pd.read_csv(sales_file)
        products_df = pd.read_csv(products_file)
        stores_df = pd.read_csv(stores_file)

        print("\nData loaded successfully")
        print("Sales Shape:", sales_df.shape)
        print("Products Shape:", products_df.shape)
        print("Stores Shape:", stores_df.shape)

        print("\nMissing Values in Sales Data:")
        print(sales_df.isnull().sum())

        duplicate_rows = sales_df.duplicated().sum()
        sales_df = sales_df.drop_duplicates().copy()

        sales_df["quantity"] = sales_df["quantity"].fillna(0)
        sales_df = sales_df.dropna(subset=["amount"]).copy()

        sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"])
        sales_df["amount"] = sales_df["amount"].astype(float)
        sales_df["quantity"] = sales_df["quantity"].astype(int)

        print("\nDuplicate rows removed:", duplicate_rows)
        print("Cleaned Sales Data Shape:", sales_df.shape)

        sales_df["product_id"] = sales_df["product_id"].astype(str).str.strip()
        products_df["product_id"] = products_df["product_id"].astype(str).str.strip()

        sales_df["store_id"] = sales_df["store_id"].astype(str).str.strip()
        stores_df["store_id"] = stores_df["store_id"].astype(str).str.strip()

        final_df = pd.merge(sales_df, products_df, on="product_id", how="left")
        final_df = pd.merge(final_df, stores_df, on="store_id", how="left")

        final_df["total_revenue"] = np.multiply(final_df["quantity"], final_df["price"])

        print("\nFinal Merged Data:")
        print(final_df)

        print("\nRevenue Summary:")
        print("Mean Revenue:", np.nanmean(final_df["total_revenue"]))
        print("Max Revenue:", np.nanmax(final_df["total_revenue"]))
        print("Min Revenue:", np.nanmin(final_df["total_revenue"]))

        city_revenue = final_df.groupby("city")["total_revenue"].sum()
        city_revenue = city_revenue.sort_values(ascending=False)

        print("\nTotal Revenue Per City:")
        print(city_revenue)

        os.makedirs("output", exist_ok=True)

        conn = sqlite3.connect("output/retail_sales.db")

        final_df.to_sql("retail_sales", conn, if_exists="replace", index=False)

        print("\nData loaded into SQLite table: retail_sales")

        top_products_query = """
        SELECT 
            product_name,
            SUM(quantity) AS total_quantity_sold
        FROM retail_sales
        WHERE product_name IS NOT NULL
        GROUP BY product_name
        ORDER BY total_quantity_sold DESC
        LIMIT 3;
        """

        top_products = pd.read_sql_query(top_products_query, conn)

        print("\nTop 3 Best Selling Products:")
        print(top_products)

        store_query = """
        SELECT 
            store_name,
            sale_date,
            SUM(total_revenue) AS daily_revenue
        FROM retail_sales
        WHERE store_name IS NOT NULL
        GROUP BY store_name, sale_date
        ORDER BY sale_date;
        """

        store_report = pd.read_sql_query(store_query, conn)

        print("\nTotal Revenue Per Store Per Day:")
        print(store_report)

        conn.close()

        valid_data = final_df.dropna(subset=["product_name", "store_name"])

        print("\nSummary Report")
        print("Total Number of Transactions:", valid_data.shape[0])
        print("Total Revenue:", valid_data["total_revenue"].sum())
        print("Top Selling City:", valid_data.groupby("city")["total_revenue"].sum().idxmax())
        print("Top Selling Product:", valid_data.groupby("product_name")["quantity"].sum().idxmax())

        final_df.to_csv("output/final_cleaned_data.csv", index=False)
        city_revenue.to_csv("output/city_revenue_report.csv")
        top_products.to_csv("output/top_products_report.csv", index=False)
        store_report.to_csv("output/store_daily_revenue_report.csv", index=False)

        print("\nPipeline completed successfully")

    except FileNotFoundError:
        print("\nError: CSV file missing")
        print("Please check these files:")
        print("data/sales_data.csv")
        print("data/products.csv")
        print("data/stores.csv")

    except Exception as e:
        print("\nSome error occurred")
        print("Error:", e)


run_pipeline()




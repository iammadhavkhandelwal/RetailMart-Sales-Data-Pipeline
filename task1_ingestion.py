import pandas as pd

# loading all csv files
sales_df = pd.read_csv("data/sales_data.csv")
products_df = pd.read_csv("data/products.csv")
stores_df = pd.read_csv("data/stores.csv")

print("DATA INGESTION")

print("\nSales Data Shape:", sales_df.shape)
print(sales_df.head())

print("\nProducts Data Shape:", products_df.shape)
print(products_df.head())

print("\nStores Data Shape:", stores_df.shape)
print(stores_df.head())

print("\nMissing Values in Sales Data:")
print(sales_df.isnull().sum())

print("\nColumns having null values in Sales Data:")
print(sales_df.isnull().sum()[sales_df.isnull().sum() > 0])

print("\nMissing Values in Products Data:")
print(products_df.isnull().sum())

print("\nColumns having null values in Products Data:")
print(products_df.isnull().sum()[products_df.isnull().sum() > 0])

print("\nMissing Values in Stores Data:")
print(stores_df.isnull().sum())

print("\nColumns having null values in Stores Data:")
print(stores_df.isnull().sum()[stores_df.isnull().sum() > 0])
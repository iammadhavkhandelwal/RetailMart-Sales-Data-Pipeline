# RetailMart Sales Data Pipeline

## Project Description

I am a final-year B.Tech student and I created this project as part of my Data Engineering assignment. The project is based on RetailMart sales data, where the company collects daily sales data from different stores.

In this project, I worked with three CSV files:

* `sales_data.csv`
* `products.csv`
* `stores.csv`

The sales data contains some common real-world data issues like missing values, duplicate records, and data type problems. The main goal of this project is to clean the raw data, merge it with product and store details, calculate revenue, and store the final cleaned data into a SQLite database for reporting.

## How I Came to This Solution

First, I read the problem statement carefully and understood that the main requirement was to build a small data pipeline. The data was available in multiple CSV files, so I decided to follow a simple ETL approach.

ETL means:

* Extract: Load data from CSV files
* Transform: Clean and process the data
* Load: Store the final data into a database

After understanding the tasks, I divided the complete project into separate Python files. I did this because each task in the assignment can be checked separately. After completing all individual tasks, I also created a final pipeline file that runs all steps in one function.

My solution flow is:

```text
CSV Files
   ↓
Load Data
   ↓
Clean Data
   ↓
Merge Data
   ↓
Calculate Revenue
   ↓
Load into SQLite
   ↓
Generate Reports
```

## Project Approach

I followed a step-by-step approach for this project.

First, I created three CSV files with sample data. I intentionally added missing values and duplicate rows in `sales_data.csv` because the assignment required raw and messy data.

Then I completed each task separately:

* Task 1: Data Ingestion
* Task 2: Data Cleaning
* Task 3: Data Transformation
* Task 4: Data Loading into SQLite
* Task 5: Reporting and Insights
* Task 6: Pipeline and Error Handling

This helped me test every part of the project properly.

## Tech Stack Used

### Python

I used Python as the main programming language because it is simple, easy to understand, and commonly used in data engineering and data analysis tasks.

### Pandas

I used Pandas for reading CSV files, checking missing values, removing duplicate records, cleaning data, merging datasets, and creating output reports.

Reason for using Pandas:

* Easy to work with CSV files
* Useful for data cleaning
* Simple DataFrame operations
* Good for grouping and merging data

### NumPy

I used NumPy to calculate the `total_revenue` column and to calculate summary values like mean, maximum, and minimum revenue.

Reason for using NumPy:

* It is useful for numerical calculations
* The assignment asked to use NumPy for revenue calculations

### SQLite

I used SQLite to store the final cleaned and merged data.

Reason for using SQLite:

* It is lightweight
* No separate server setup is needed
* Good for small assignment-level projects
* Easy to connect with Python using `sqlite3`

### SQL

I used SQL queries to generate business reports from the final `retail_sales` table.

Reason for using SQL:

* SQL is useful for reporting
* It helps in finding top-selling products
* It helps in calculating revenue per store per day

### VS Code

I used VS Code for writing and running Python scripts.

Reason for using VS Code:

* Easy file management
* Integrated terminal
* Good for Python project development

## Project Folder Structure

```text
RetailMart_Assignment/
│
├── data/
│   ├── sales_data.csv
│   ├── products.csv
│   └── stores.csv
│
├── output/
│   ├── cleaned_sales_data.csv
│   ├── final_cleaned_data.csv
│   ├── city_revenue_report.csv
│   ├── top_products_report.csv
│   ├── store_daily_revenue_report.csv
│   └── retail_sales.db
│
├── task1_ingestion.py
├── task2_cleaning.py
├── task3_transformation.py
├── task4_sql_loading.py
├── task5 reporting & Insights.py
├── Task6 Pipeline & error handling.py
├── requirements.txt
└── README.md
```

## Dataset Details

### 1. sales_data.csv

This file contains daily sales transaction data.

Columns used:

* `sale_id`
* `store_id`
* `product_id`
* `quantity`
* `sale_date`
* `amount`

This file contains missing values and duplicate records to simulate real-world data issues.

### 2. products.csv

This file contains product information.

Columns used:

* `product_id`
* `product_name`
* `category`
* `price`

### 3. stores.csv

This file contains store information.

Columns used:

* `store_id`
* `store_name`
* `city`
* `region`

## Task-wise Explanation

## Task 1: Data Ingestion

In this task, I loaded all three CSV files into Pandas DataFrames.

Files loaded:

* `sales_data.csv`
* `products.csv`
* `stores.csv`

I printed the shape of each DataFrame to check the number of rows and columns.

I also printed the first 5 rows of each DataFrame using `.head()` to understand the structure of the data.

After that, I checked missing values in all three DataFrames using:

```python
df.isnull().sum()
```

I also printed only those columns that had null values.

This task helped me understand the quality and structure of the raw data before cleaning.

Output checked in this task:

* Shape of sales data
* Shape of products data
* Shape of stores data
* First 5 rows of each file
* Missing value summary
* Columns having null values

Python file used:

```text
task1_ingestion.py
```

## Task 2: Data Cleaning

In this task, I cleaned the `sales_data.csv` file because sales data had missing values and duplicate rows.

First, I counted duplicate rows using:

```python
sales_df.duplicated().sum()
```

Then I removed duplicate rows using:

```python
sales_df.drop_duplicates()
```

After that, I filled missing values in the `quantity` column with 0 because missing quantity means no quantity was recorded.

```python
sales_df["quantity"] = sales_df["quantity"].fillna(0)
```

Then I removed rows where `amount` was NULL because without amount, the sales record is not useful for revenue calculation.

```python
sales_df = sales_df.dropna(subset=["amount"])
```

I also converted `sale_date` into datetime format and `amount` into float type.

```python
sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"], errors="coerce")
sales_df["amount"] = sales_df["amount"].astype(float)
```

Finally, I saved the cleaned sales data into the output folder as:

```text
output/cleaned_sales_data.csv
```

This cleaned file is used in the next task.

Python file used:

```text
task2_cleaning.py
```

## Task 3: Data Transformation

In this task, I merged the cleaned sales data with product and store data.

First, I loaded:

* `output/cleaned_sales_data.csv`
* `data/products.csv`
* `data/stores.csv`

Before merging, I converted `product_id` and `store_id` into string format to avoid merge errors.

Then I merged sales data with product data using `product_id`.

```python
final_df = pd.merge(sales_df, products_df, on="product_id", how="left")
```

After that, I merged the result with store data using `store_id`.

```python
final_df = pd.merge(final_df, stores_df, on="store_id", how="left")
```

After merging, I created a new column called `total_revenue`.

Formula used:

```text
total_revenue = quantity * price
```

Code used:

```python
final_df["total_revenue"] = np.multiply(final_df["quantity"], final_df["price"])
```

Then I calculated:

* Mean revenue
* Maximum revenue
* Minimum revenue

I also grouped the data by city and calculated total revenue per city.

```python
city_revenue = final_df.groupby("city")["total_revenue"].sum()
```

The city revenue report was sorted in descending order.

Output files generated:

```text
output/final_cleaned_data.csv
output/city_revenue_report.csv
```

Python file used:

```text
task3_transformation.py
```

## Task 4: Data Loading into SQLite

In this task, I loaded the final cleaned and merged data into a SQLite database.

First, I read:

```text
output/final_cleaned_data.csv
```

Then I created a SQLite database file:

```text
output/retail_sales.db
```

I loaded the final DataFrame into a table named:

```text
retail_sales
```

Code used:

```python
final_df.to_sql("retail_sales", conn, if_exists="replace", index=False)
```

After loading the data, I wrote a SQL query to find the Top 3 best-selling products by total quantity sold.

SQL query used:

```sql
SELECT 
    product_name,
    SUM(quantity) AS total_quantity_sold
FROM retail_sales
WHERE product_name IS NOT NULL
GROUP BY product_name
ORDER BY total_quantity_sold DESC
LIMIT 3;
```

The output was saved as:

```text
output/top_products_report.csv
```

Python file used:

```text
task4_sql_loading.py
```

## Task 5: Reporting and Insights

In this task, I generated reports from the `retail_sales` table.

First, I wrote a SQL query to find total revenue per store per day.

SQL query used:

```sql
SELECT 
    store_name,
    sale_date,
    SUM(total_revenue) AS daily_revenue
FROM retail_sales
WHERE store_name IS NOT NULL
GROUP BY store_name, sale_date
ORDER BY sale_date;
```

This report was saved as:

```text
output/store_daily_revenue_report.csv
```

After that, I printed a summary report using Python.

The summary report includes:

* Total number of transactions
* Total revenue
* Top selling city
* Top selling product

This helped in understanding the final business insights from the cleaned data.

Python file used:

```text
task5 reporting & Insights.py
```

## Task 6: Pipeline and Error Handling

In this task, I created a final pipeline function named:

```python
run_pipeline()
```

The purpose of this function is to run all major steps in one place.

The pipeline follows this flow:

```text
load data → clean data → transform data → load to database → generate reports
```

I also added basic error handling using `try-except`.

If any CSV file is missing, the program does not crash. Instead, it prints a proper error message.

Example:

```text
Error: CSV file missing
Please check data/sales_data.csv
Please check data/products.csv
Please check data/stores.csv
```

This makes the project more reliable and easy to run.

Python file used:

```text
Task6 Pipeline & error handling.py
```

## Output Files Explanation

### cleaned_sales_data.csv

This file contains sales data after removing duplicates, filling missing quantity values, removing rows with missing amount, and converting data types.

### final_cleaned_data.csv

This file contains the final merged dataset after combining sales, product, and store data.

### city_revenue_report.csv

This report shows total revenue generated by each city.

### top_products_report.csv

This report shows the top 3 best-selling products by quantity sold.

### store_daily_revenue_report.csv

This report shows total revenue per store per day.

### retail_sales.db

This is the SQLite database file that stores the final cleaned data in the `retail_sales` table.

## How to Run the Project

First install the required libraries:

```bash
pip install -r requirements.txt
```

Run the files step by step:

```bash
python task1_ingestion.py
python task2_cleaning.py
python task3_transformation.py
python task4_sql_loading.py
python "task5 reporting & Insights.py"
python "Task6 Pipeline & error handling.py"
```

## requirements.txt

The project requires these libraries:

```text
pandas
numpy
```

SQLite is already available with Python through the `sqlite3` module, so no extra installation is required for SQLite.

## Final Output

The final cleaned and merged data is stored in SQLite database table:

```text
retail_sales
```

The project generates the following business reports:

* Top 3 best-selling products
* Total revenue per store per day
* City-wise revenue
* Final summary report

## Project Links

GitHub Repository Link:
(https://github.com/iammadhavkhandelwal/RetailMart-Sales-Data-Pipeline.git)

## What I Learned

Through this project, I learned how a basic Data Engineering ETL pipeline works. I understood how to load data from CSV files, check missing values, remove duplicates, clean data, merge multiple datasets, calculate revenue, load data into SQLite, and generate SQL reports.

I also learned why error handling is important in a data pipeline. If a file is missing or data has an issue, the pipeline should show a proper message instead of crashing.

## Conclusion

This project gave me practical understanding of data ingestion, data cleaning, data transformation, database loading, SQL reporting, and pipeline automation. It helped me understand how raw business data can be converted into clean and useful reports for decision-making.

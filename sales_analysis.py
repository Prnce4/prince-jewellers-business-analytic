import pandas as pd
import matplotlib.pyplot as plt

# Load sales data
FILE_PATH = "data.xlsx"

df = pd.read_excel(
    FILE_PATH,
    sheet_name="Sales_Transactions"
)

# Prepare bill dates
df["Bill Date"] = pd.to_datetime(
    df["Bill Date"],
    errors="coerce"
)

print("\nSales Data Analysis")
print("=" * 40)
print("Dataset shape:", df.shape)
print("Invalid bill dates:", df["Bill Date"].isna().sum())

# Calculate monthly sales
df["Month"] = df["Bill Date"].dt.to_period("M")

monthly_sales = (
    df.groupby("Month")["Final Item Amount"]
    .sum()
)

print("\nMonthly Sales Revenue:")
print(monthly_sales.round(2).to_string())

# Calculate monthly sales growth
monthly_growth = monthly_sales.pct_change() * 100

print("\nMonthly Sales Growth (%):")
print(monthly_growth.round(2).to_string())

# Analyze sales by category
category_sales = (
    df.groupby("Category")["Final Item Amount"]
    .sum()
    .sort_values(ascending=False)
)

total_sales = category_sales.sum()

category_contribution = (
    category_sales / total_sales * 100
    if total_sales != 0
    else category_sales * 0
)

print("\nCategory-wise Sales Revenue:")
print(category_sales.round(2).to_string())

print("\nCategory Sales Contribution (%):")
print(category_contribution.round(2).to_string())

# Analyze quantity and average revenue by category
category_summary = df.groupby("Category").agg(
    Total_Quantity=("Quantity", "sum"),
    Average_Revenue_Per_Record=("Final Item Amount", "mean"),
    Sales_Records=("Bill Number", "size")
).sort_values(
    "Average_Revenue_Per_Record",
    ascending=False
)

print("\nCategory-wise Sales Summary:")
print(category_summary.round(2).to_string())

# Analyze monthly sales by category
monthly_category_sales = df.pivot_table(
    index="Month",
    columns="Category",
    values="Final Item Amount",
    aggfunc="sum",
    fill_value=0
)

monthly_category_sales = monthly_category_sales.dropna(axis=0, how="all")

print("\nMonthly Revenue by Category:")
print(monthly_category_sales.round(2).to_string())

monthly_total = monthly_category_sales.sum(axis=1)

monthly_category_share = (
    monthly_category_sales
    .div(monthly_total.where(monthly_total.ne(0)), axis=0)
    * 100
)

print("\nMonthly Category Revenue Share (%):")
print(monthly_category_share.round(2).to_string())

# Plot monthly sales revenue
if not monthly_sales.empty:
    monthly_sales.plot(
        kind="line",
        marker="o",
        figsize=(10, 5),
        title="Monthly Sales Revenue"
    )

    plt.xlabel("Month")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Analyze customer revenue
customer_revenue = (
    df.groupby("Customer ID")["Final Item Amount"]
    .sum()
    .sort_values(ascending=False)
)

print("\nTop 10 Customers by Revenue:")
print(customer_revenue.head(10).round(2).to_string())

top_10_revenue = customer_revenue.head(10).sum()
total_revenue = df["Final Item Amount"].sum()

top_10_share = (
    top_10_revenue / total_revenue * 100
    if total_revenue != 0
    else 0
)

print(f"\nTop 10 Customers' Revenue: ₹{top_10_revenue:,.2f}")
print(f"Total Sales Revenue: ₹{total_revenue:,.2f}")
print(f"Top 10 Customers' Revenue Share: {top_10_share:.2f}%")

# Analyze customer purchase frequency
customer_bills = (
    df.groupby("Customer ID")["Bill Number"]
    .nunique()
)

total_customers = df["Customer ID"].nunique()

one_time_customers = (customer_bills == 1).sum()
repeat_customers = (customer_bills > 1).sum()

repeat_percentage = (
    repeat_customers / total_customers * 100
    if total_customers != 0
    else 0
)

print("\nCustomer Purchase Frequency")
print("Total unique customers:", total_customers)
print("Customers with one bill:", one_time_customers)
print("Customers with multiple bills:", repeat_customers)
print(f"Repeat-customer percentage: {repeat_percentage:.2f}%")

print("\nTotal unique bills:", df["Bill Number"].nunique())

print("\nBills per Customer:")
print(customer_bills.value_counts().sort_index().to_string())

print("\nSample Customer Bill Counts:")
print(customer_bills.head(10).to_string())

# Calculate average revenue per customer
average_customer_revenue = (
    total_revenue / total_customers
    if total_customers != 0
    else 0
)

print(
    f"\nAverage Revenue Per Customer: "
    f"₹{average_customer_revenue:,.2f}"
)

print("\nSales analysis completed.")

import pandas as pd
import matplotlib.pyplot as plt

# Load purchase and artisan data
FILE_PATH = "data.xlsx"

df = pd.read_excel(
    FILE_PATH,
    sheet_name="Purchases_and_Artisan"
)

numeric_columns = [
    "Weight g",
    "Making Labour Cost",
    "Total Cost",
    "Amount Paid",
    "Pending Balance",
]

# Check dataset details
print("\nPurchase and Artisan Data Overview")
print("=" * 40)

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nSample records:")
print(df.head().to_string(index=False))

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nColumn data types:")
print(df.dtypes.to_string())

print(
    "\nDuplicate purchase reference IDs:",
    df["Purchase Ref ID"].duplicated().sum()
)

# Check numeric values
print("\nNegative values:")
print((df[numeric_columns] < 0).sum().to_string())

# Validate pending balances
expected_pending = df["Total Cost"] - df["Amount Paid"]

balance_mismatch = (
    expected_pending - df["Pending Balance"]
).abs() > 0.01

overpaid_records = (
    df["Amount Paid"] > df["Total Cost"] + 0.01
)

print("\nFinancial Validation")
print(
    "Incorrect pending balances:",
    balance_mismatch.sum()
)
print(
    "Records with overpayment:",
    overpaid_records.sum()
)

# Check purchase types and categories
print("\nPurchase Types:")
print(df["Type"].value_counts(dropna=False).to_string())

print("\nCategories:")
print(df["Category"].value_counts(dropna=False).to_string())

print("\nType vs Category:")
print(
    pd.crosstab(
        df["Type"],
        df["Category"],
        dropna=False
    ).to_string()
)

# Summarize weight and labour costs by type
type_summary = df.groupby("Type", dropna=False).agg(
    Record_Count=("Purchase Ref ID", "count"),
    Total_Weight_g=("Weight g", "sum"),
    Average_Weight_g=("Weight g", "mean"),
    Total_Labour_Cost=("Making Labour Cost", "sum"),
    Average_Labour_Cost=("Making Labour Cost", "mean"),
)

print("\nWeight and Labour Cost by Type:")
print(type_summary.round(2).to_string())

# Check zero values
print("\nZero-weight records by type:")
print(
    df.loc[df["Weight g"].eq(0), "Type"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nZero-labour-cost records by type:")
print(
    df.loc[df["Making Labour Cost"].eq(0), "Type"]
    .value_counts(dropna=False)
    .to_string()
)

print(
    "\nRecords with zero total cost:",
    df["Total Cost"].eq(0).sum()
)

# Summarize costs and payments by type
cost_summary = df.groupby("Type", dropna=False).agg(
    Total_Cost=("Total Cost", "sum"),
    Amount_Paid=("Amount Paid", "sum"),
    Pending_Balance=("Pending Balance", "sum"),
    Labour_Cost=("Making Labour Cost", "sum"),
)

cost_summary["Labour_Cost_Percent"] = (
    cost_summary["Labour_Cost"]
    .div(cost_summary["Total_Cost"].where(cost_summary["Total_Cost"].ne(0)))
    .mul(100)
)

print("\nCost Summary by Type:")
print(cost_summary.round(2).to_string())

# Analyze monthly costs
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\nRecords with invalid dates:", df["Date"].isna().sum())

df["Month"] = df["Date"].dt.to_period("M")

monthly_cost = df.pivot_table(
    index="Month",
    columns="Type",
    values="Total Cost",
    aggfunc="sum",
    fill_value=0
)

print("\nMonthly Cost by Type:")
print(monthly_cost.round(2).to_string())

monthly_total = df.groupby("Month")["Total Cost"].sum()

print("\nTotal Monthly Spending:")
print(monthly_total.round(2).to_string())

# Plot monthly costs
if not monthly_total.empty:
    monthly_total.plot(
        kind="bar",
        figsize=(10, 5),
        title="Monthly Purchase and Artisan Costs"
    )

    plt.xlabel("Month")
    plt.ylabel("Total Cost (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Validate artisan job work costs
artisan_df = df[df["Type"].eq("Artisan Job Work")]

artisan_total_cost = artisan_df["Total Cost"].sum()
artisan_labour_cost = artisan_df["Making Labour Cost"].sum()

print("\nArtisan Cost Validation")
print("Artisan records:", len(artisan_df))
print(f"Total artisan cost: ₹{artisan_total_cost:,.2f}")
print(f"Total artisan labour charges: ₹{artisan_labour_cost:,.2f}")
print(
    "Cost and labour totals match:",
    abs(artisan_total_cost - artisan_labour_cost) < 0.01
)

print("\nPurchase analysis completed.")

import pandas as pd
import matplotlib.pyplot as plt

# Load shop expense data
FILE_PATH = "data.xlsx"

df = pd.read_excel(
    FILE_PATH,
    sheet_name="Shop_Expenses"
)

# Check dataset details
print("\nShop Expense Data Overview")
print("=" * 40)

print("Dataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nSample records:")
print(df.head().to_string(index=False))

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nDuplicate expense IDs:", df["Expense ID"].duplicated().sum())

print("\nColumn data types:")
print(df.dtypes.to_string())

# Check expense amounts
print("\nNegative expense amounts:", df["Amount"].lt(0).sum())
print("Zero expense amounts:", df["Amount"].eq(0).sum())

# Check expense statuses
print("\nExpense Status Counts:")
print(df["Status"].value_counts(dropna=False).to_string())

# Analyze expenses by category
print("\nExpense Category Counts:")
print(df["Category"].value_counts(dropna=False).to_string())

category_summary = df.groupby("Category", dropna=False).agg(
    Expense_Count=("Expense ID", "count"),
    Total_Expense=("Amount", "sum"),
    Average_Expense=("Amount", "mean")
).sort_values(
    "Total_Expense",
    ascending=False
)

print("\nExpense Summary by Category:")
print(category_summary.round(2).to_string())

total_expenses = df["Amount"].sum()

print(f"\nTotal Recorded Expenses: ₹{total_expenses:,.2f}")

# Analyze monthly expenses
df["Date"] = pd.to_datetime(
    df["Date"],
    errors="coerce"
)

print("\nRecords with invalid dates:", df["Date"].isna().sum())

df["Month"] = df["Date"].dt.to_period("M")

monthly_expenses = df.groupby("Month")["Amount"].sum()

print("\nMonthly Expenses:")
print(monthly_expenses.round(2).to_string())

# Plot monthly expenses
if not monthly_expenses.empty:
    monthly_expenses.plot(
        kind="bar",
        figsize=(10, 5),
        title="Monthly Shop Expenses"
    )

    plt.xlabel("Month")
    plt.ylabel("Expense Amount (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Check expense date range
print("\nExpense Date Range:")
print("First expense date:", df["Date"].min())
print("Last expense date:", df["Date"].max())

# Summarize expenses by status
status_summary = df.groupby("Status", dropna=False).agg(
    Record_Count=("Expense ID", "count"),
    Total_Amount=("Amount", "sum")
)

print("\nExpense Status Summary:")
print(status_summary.round(2).to_string())

# Validate expense totals
monthly_total = monthly_expenses.sum()

print("\nTotal Validation")
print(f"Overall expense total: ₹{total_expenses:,.2f}")
print(f"Sum of monthly totals: ₹{monthly_total:,.2f}")
print(
    "Totals match:",
    abs(total_expenses - monthly_total) < 0.01
)

print("\nShop expense analysis completed.")

import pandas as pd

# Load customer payment data
FILE_PATH = "data.xlsx"

df = pd.read_excel(
    FILE_PATH,
    sheet_name="Customer_Payments"
)

# Check dataset details
print("\nPayment Data Overview")
print("=" * 40)

print("Dataset shape:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nSample records:")
print(df.head().to_string(index=False))

print("\nMissing values:")
print(df.isna().sum().to_string())

print("\nDuplicate payment IDs:", df["Payment ID"].duplicated().sum())

# Validate payment balances
expected_balance = (
    df["Total Bill Amount"] - df["Amount Received"]
)

incorrect_balance = (
    expected_balance - df["Remaining Balance"]
).abs() > 0.01

print("\nInconsistent balance records:", incorrect_balance.sum())

# Calculate overall payment summary
total_bill_amount = df["Total Bill Amount"].sum()
total_received = df["Amount Received"].sum()
total_balance = df["Remaining Balance"].sum()

collection_percentage = (
    total_received / total_bill_amount * 100
    if total_bill_amount != 0
    else 0
)

print("\nOverall Payment Summary")
print(f"Total Bill Amount: ₹{total_bill_amount:,.2f}")
print(f"Total Amount Received: ₹{total_received:,.2f}")
print(f"Total Remaining Balance: ₹{total_balance:,.2f}")
print(f"Collection Percentage: {collection_percentage:.2f}%")

# Analyze collections by payment method
payment_summary = df.groupby("Payment Method").agg(
    Total_Received=("Amount Received", "sum"),
    Total_Balance=("Remaining Balance", "sum"),
    Transaction_Count=("Payment ID", "count")
)

payment_summary["Collection_Share_Percent"] = (
    payment_summary["Total_Received"]
    / total_received * 100
    if total_received != 0
    else 0
)

print("\nPayment Method Analysis")
print(payment_summary.round(2).to_string())

# Analyze outstanding payments
pending_payments = df[df["Remaining Balance"] > 0]

customer_outstanding = (
    pending_payments.groupby("Customer ID")
    .agg(
        Pending_Balance=("Remaining Balance", "sum"),
        Pending_Records=("Payment ID", "count")
    )
    .sort_values("Pending_Balance", ascending=False)
)

print("\nOutstanding Payment Analysis")
print("Records with pending balance:", len(pending_payments))
print("Customers with pending balance:", len(customer_outstanding))

print("\nTop 10 Customers by Outstanding Balance:")
print(customer_outstanding.head(10).round(2).to_string())

# Load sales data for reconciliation
sales_df = pd.read_excel(
    FILE_PATH,
    sheet_name="Sales_Transactions"
)

# Compare bills across both datasets
payment_bills = set(df["Bill Number"].dropna().unique())
sales_bills = set(sales_df["Bill Number"].dropna().unique())

unmatched_payment_bills = payment_bills - sales_bills
missing_payment_bills = sales_bills - payment_bills

print("\nSales and Payment Reconciliation")
print("Unique payment bills:", len(payment_bills))
print("Unique sales bills:", len(sales_bills))
print("Payment bills missing from sales:", len(unmatched_payment_bills))
print("Sales bills missing from payments:", len(missing_payment_bills))

# Compare bill amounts between datasets
sales_bill_totals = (
    sales_df.groupby("Bill Number")["Final Item Amount"].sum()
)

payment_bill_totals = (
    df.groupby("Bill Number")["Total Bill Amount"].first()
)

bill_comparison = pd.concat(
    [
        sales_bill_totals.rename("Sales_Amount"),
        payment_bill_totals.rename("Payment_Bill_Amount")
    ],
    axis=1
)

bill_comparison["Difference"] = (
    bill_comparison["Sales_Amount"]
    - bill_comparison["Payment_Bill_Amount"]
)

# Identify bills with mismatched amounts
mismatched_bills = bill_comparison[
    bill_comparison["Difference"].abs() > 0.01
]

print("\nBill Amount Validation")
print("Bills compared:", len(bill_comparison))
print("Bills with amount mismatches:", len(mismatched_bills))

if not mismatched_bills.empty:
    print("\nSample mismatched bills:")
    print(mismatched_bills.head(10).round(2).to_string())

print("\nPayment analysis completed.")

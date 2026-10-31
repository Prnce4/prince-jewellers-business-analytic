import pandas as pd

file_path = "data.xlsx"

sales = pd.read_excel(file_path, sheet_name="Sales_Transactions")
payments = pd.read_excel(file_path, sheet_name="Customer_Payments")
purchases = pd.read_excel(file_path, sheet_name="Purchases_and_Artisan")
expenses = pd.read_excel(file_path, sheet_name="Shop_Expenses")

total_sales = sales["Final Item Amount"].sum()
total_received = payments["Amount Received"].sum()
total_outstanding = payments["Remaining Balance"].sum()

total_purchase_cost = purchases["Total Cost"].sum()
total_shop_expenses = expenses["Amount"].sum()

print("\nPRINCE JEWELLERS - BUSINESS SUMMARY")
print("----------------------------------")

print(f"Total Sales Revenue: Rs. {total_sales:,.2f}")
print(f"Amount Received: Rs. {total_received:,.2f}")
print(f"Outstanding Balance: Rs. {total_outstanding:,.2f}")
print(f"Total Purchase Cost: Rs. {total_purchase_cost:,.2f}")
print(f"Total Shop Expenses: Rs. {total_shop_expenses:,.2f}")

if total_sales > 0:
    collection_rate = (total_received / total_sales) * 100
    print(f"Collection Rate: {collection_rate:.2f}%")

print("\nNote: This summary does not calculate actual profit.")

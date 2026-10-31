import pandas as pd

# Load sales data
FILE_PATH = "data.xlsx"
SHEET_NAME = "Sales_Transactions"

df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)

numeric_columns = [
    "Gross Weight g",
    "Net Weight g",
    "Metal Rate Per g",
]

record_columns = [
    "Bill Number",
    "Category",
    "Item Description",
]

# Check dataset details
print("\nSales Data Quality Report")
print("=" * 40)

print(f"\nDataset dimensions: {df.shape}")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print("\nColumn data types:")
print(df.dtypes.to_string())

print("\nMissing values:")
print(df.isna().sum().to_string())

print(f"\nExact duplicate rows: {df.duplicated().sum()}")

# Generate numerical summary
print("\nNumerical summary:")
print(df.describe().to_string())

# Check category-wise records and missing purity
print("\nCategory-wise record counts:")
print(df["Category"].value_counts(dropna=False).to_string())

print("\nMissing purity by category:")
print(
    df.groupby("Category", dropna=False)["Purity"]
    .apply(lambda values: values.isna().sum())
    .to_string()
)

# Investigate missing purity in silver records
silver_records = df[df["Category"].eq("Silver")]

silver_missing = silver_records[silver_records["Purity"].isna()]
silver_known = silver_records[silver_records["Purity"].notna()]

silver_sample_columns = [
    "Item Description",
    "Gross Weight g",
    "Net Weight g",
    "Metal Rate Per g",
    "Final Item Amount",
]

print("\nSilver records with missing purity:")
print(f"Total records: {len(silver_missing)}")

print("\nItem descriptions:")
print(
    silver_missing["Item Description"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nSample records:")
if silver_missing.empty:
    print("No records found.")
else:
    print(
        silver_missing[silver_sample_columns]
        .head(10)
        .to_string(index=False)
    )

print("\nKnown purity values by silver item:")
if silver_known.empty:
    print("No records found.")
else:
    print(
        silver_known.groupby("Item Description", dropna=False)["Purity"]
        .value_counts(dropna=False)
        .to_string()
    )

# Check zero values in important columns
print("\nZero-value checks:")

for column in numeric_columns:
    zero_records = df[df[column].eq(0)]

    print(f"\n{column}: {len(zero_records)} records")

    if not zero_records.empty:
        print(
            zero_records[record_columns + [column]]
            .head(10)
            .to_string(index=False)
        )

        if len(zero_records) > 10:
            print(f"... and {len(zero_records) - 10} more records")

# Investigate records with zero weight
zero_weight = df[
    df["Gross Weight g"].eq(0) |
    df["Net Weight g"].eq(0)
]

print("\nZero-weight records:", len(zero_weight))

print("\nRecords by category:")
print(zero_weight["Category"].value_counts(dropna=False).to_string())

print("\nRecords by item description:")
print(
    zero_weight["Item Description"]
    .value_counts(dropna=False)
    .to_string()
)

print("\nData quality check completed.")

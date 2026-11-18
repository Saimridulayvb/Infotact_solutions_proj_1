
import pandas as pd

# List of all raw and processed CSV files
files = [
    "data/raw/providers.csv",
    "data/raw/inputs.csv",
    "data/raw/provision.csv",
    "data/raw/sequence.csv",
    "data/raw/stages.csv",
    "data/processed/selected_companies.csv",
    "data/processed/selected_relationships.csv",
    "data/processed/goes_into_relationships.csv",
    "data/processed/is_type_of_relationships.csv"
]

print("=" * 60)
print("       ATMOGRAPH - MISSING VALUE INVESTIGATION")
print("=" * 60)

# Step 1: Check missing values in every CSV file
for file in files:

    print("\nFile:", file)

    df = pd.read_csv(file)

    print("Total rows:", len(df))
    print("Total columns:", len(df.columns))

    missing_values = df.isnull().sum()
    missing_values = missing_values[missing_values > 0]

    if missing_values.empty:
        print("No missing values found.")
    else:
        print("\nMissing values:")
        print(missing_values)

# Step 2: Inspect important missing fields
df = pd.read_csv(
    "data/processed/selected_relationships.csv"
)

print("\n" + "=" * 60)
print("       DETAILED RELATIONSHIP INVESTIGATION")
print("=" * 60)

columns_to_check = [
    "stage_name",
    "share_provided",
    "source"
]

for column in columns_to_check:

    if column in df.columns:

        print("\nColumn:", column)

        missing_records = df[df[column].isnull()]

        print("Missing records:", len(missing_records))

        if not missing_records.empty:
            print("\nSample records:")
            print(missing_records.head(10).to_string(index=False))

print("\n" + "=" * 60)
print("       INVESTIGATION COMPLETED")
print("=" * 60)

print("\n" + "=" * 60)
print("FURTHER INVESTIGATION")
print("=" * 60)

# 1. Check provider records with missing country
providers = pd.read_csv("data/raw/providers.csv")

print("\nProviders with missing country:")
print(
    providers[providers["country"].isnull()]
    [["provider_name", "provider_type", "country"]]
    .head(15).to_string(index=False)
)

# 2. Check inputs that have stage information
inputs = pd.read_csv("data/raw/inputs.csv")

print("\nInputs with available stage information:")
print(
    inputs[inputs["stage_name"].notnull()]
    [["input_id", "input_name", "type", "stage_name"]]
    .to_string(index=False)
)

# 3. Inspect all six missing share records
relationships = pd.read_csv(
    "data/processed/selected_relationships.csv"
)

print("\nRelationships with missing share:")
print(
    relationships[relationships["share_provided"].isnull()]
    [["provider_name", "provided_name", "year", "source"]]
    .to_string(index=False)
)

print("\nFurther investigation completed.")

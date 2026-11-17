
import pandas as pd

# ==========================================
# STEP 1: LOAD CSV FILES
# ==========================================

providers = pd.read_csv("data/raw/providers.csv")
provision = pd.read_csv("data/raw/provision.csv")
inputs = pd.read_csv("data/raw/inputs.csv")
stages = pd.read_csv("data/raw/stages.csv")
sequence = pd.read_csv("data/raw/sequence.csv")

print("CSV files loaded successfully!")


# ==========================================
# STEP 2: FILTER ORGANIZATION RECORDS
# ==========================================

organizations = providers[
    providers["provider_type"] == "organization"
].copy()

print("\n--- ORGANIZATION DETAILS ---")
print("Total provider records:", len(providers))
print("Total organization records:", len(organizations))


# ==========================================
# STEP 3: COUNT UNIQUE INPUTS PER COMPANY
# ==========================================

company_counts = (
    provision.groupby("provider_id")["provided_id"]
    .nunique()
    .reset_index(name="connected_inputs")
)


# ==========================================
# STEP 4: ADD COMPANY DETAILS
# ==========================================

company_counts = company_counts.merge(
    organizations[["provider_id", "provider_name", "country"]],
    on="provider_id",
    how="inner"
)


# ==========================================
# STEP 5: REMOVE GENERIC ENTRIES
# ==========================================

company_counts = company_counts[
    company_counts["provider_name"] != "Various companies"
]


# ==========================================
# STEP 6: REMOVE DUPLICATE PROVIDER IDs
# ==========================================

company_counts = company_counts.drop_duplicates(
    subset="provider_id"
)


# ==========================================
# STEP 7: SORT COMPANIES
# ==========================================

company_counts = company_counts.sort_values(
    by="connected_inputs",
    ascending=False
)


# ==========================================
# STEP 8: DISPLAY TOP 20 COMPANIES
# ==========================================

print("\n--- TOP 20 CONNECTED COMPANIES ---")

print(
    company_counts.head(20).to_string(index=False)
)


# ==========================================
# STEP 9: SELECT TOP 20 COMPANIES
# ==========================================

selected_companies = company_counts.head(20).copy()


# ==========================================
# STEP 10: SAVE SELECTED COMPANIES
# ==========================================

selected_companies.to_csv(
    "data/processed/selected_companies.csv",
    index=False
)

print("\nSelected companies saved successfully!")
print("Total selected companies:", len(selected_companies))


# ==========================================
# STEP 11: EXTRACT THEIR SUPPLY RELATIONSHIPS
# ==========================================

selected_ids = selected_companies["provider_id"].unique()

selected_provision = provision[
    provision["provider_id"].isin(selected_ids)
].copy()


# ==========================================
# STEP 12: CONNECT RELATIONSHIPS WITH INPUT DATA
# ==========================================

relationships = selected_provision.merge(
    inputs[["input_id", "input_name", "type", "stage_name"]],
    left_on="provided_id",
    right_on="input_id",
    how="left"
)


# ==========================================
# STEP 13: DISPLAY SUPPLY RELATIONSHIPS
# ==========================================

print("\n--- SELECTED COMPANY SUPPLY RELATIONSHIPS ---")

print(
    relationships[
        ["provider_name", "provider_id",
         "provided_name", "input_name",
         "type", "stage_name"]
    ].head(20).to_string(index=False)
)


# ==========================================
# STEP 14: SAVE RELATIONSHIPS
# ==========================================

relationships.to_csv(
    "data/processed/selected_relationships.csv",
    index=False
)

print("\nRelationships saved successfully!")
print("Total relationship records:", len(relationships))


# ==========================================
# STEP 15: VALIDATE THE RELATIONSHIPS
# ==========================================

print("\n--- DATA VALIDATION ---")

# Check missing values
print("\nMissing values:")
print(relationships.isnull().sum())

# Check duplicate relationships
duplicate_count = relationships.duplicated(
    subset=["provider_id", "provided_id", "year"]
).sum()

print("\nDuplicate relationship records:", duplicate_count)

# Check input type distribution
print("\nInput type distribution:")
print(relationships["type"].value_counts(dropna=False))

# Check relationships per company
print("\nRelationships per company:")

print(
    relationships.groupby("provider_name")["provided_id"]
    .nunique()
    .sort_values(ascending=False)
)


# ==========================================
# STEP 16: DISPLAY FINAL SUMMARY
# ==========================================

print("\n========== FINAL SUMMARY ==========")

print("Organizations available:", len(organizations))
print("Companies selected:", len(selected_companies))
print("Supply relationship records:", len(relationships))

print(
    "Unmatched input records:",
    relationships["input_name"].isna().sum()
)

print("\nAll operations completed successfully!")
print("\n--- INPUT STAGE INSPECTION ---")

print(
    inputs[["input_id", "input_name", "type", "stage_name", "stage_id"]]
    .head(20)
    .to_string(index=False)
)

print("\nAvailable production stages:")
print(stages[["stage_id", "stage_name"]])

# STEP 17: Inspect production sequence relationships

print("\n--- SEQUENCE DATA INSPECTION ---")

print("\nFirst 15 sequence records:")

print(sequence.head(15).to_string(index=False))

print("\nSequence columns:")
print(sequence.columns.tolist())

print("\nMissing values in sequence:")
print(sequence.isnull().sum())

print("\nTotal sequence records:", len(sequence))

# STEP 18: Separate sequence relationships

goes_into = sequence.dropna(
    subset=["goes_into_id"]
).copy()

is_type_of = sequence.dropna(
    subset=["is_type_of_id"]
).copy()

print("\n--- GOES INTO RELATIONSHIPS ---")

print("Total:", len(goes_into))

print(
    goes_into[
        ["input_name", "goes_into_name"]
    ].head(10).to_string(index=False)
)

print("\n--- IS TYPE OF RELATIONSHIPS ---")

print("Total:", len(is_type_of))

print(
    is_type_of[
        ["input_name", "is_type_of_name"]
    ].head(10).to_string(index=False)
)

# STEP 19: Save GOES_INTO relationships

goes_into_clean = goes_into[
    ["input_id", "input_name", "goes_into_id", "goes_into_name"]
].copy()

goes_into_clean.to_csv(
    "data/processed/goes_into_relationships.csv",
    index=False
)


# STEP 20: Save IS_TYPE_OF relationships

is_type_of_clean = is_type_of[
    ["input_id", "input_name", "is_type_of_id", "is_type_of_name"]
].copy()

is_type_of_clean.to_csv(
    "data/processed/is_type_of_relationships.csv",
    index=False
)

print("\nSequence relationship files saved successfully!")

print("GOES_INTO records:", len(goes_into_clean))
print("IS_TYPE_OF records:", len(is_type_of_clean))

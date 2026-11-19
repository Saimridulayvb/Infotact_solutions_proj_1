
import pandas as pd
from pathlib import Path

# File paths
RAW_FILE = Path("data/raw/providers.csv")
SELECTED_FILE = Path("data/processed/selected_companies.csv")
OUTPUT_FILE = Path("data/processed/cleaned_companies.csv")

# Load datasets
providers = pd.read_csv(RAW_FILE)
selected = pd.read_csv(SELECTED_FILE)

# Select only the companies already shortlisted
selected_ids = selected["provider_id"].unique()

company_records = providers[
    providers["provider_id"].isin(selected_ids)
].copy()

# Verify consistency before deduplication
for column in ["provider_name", "provider_type", "country"]:
    conflicts = (
        company_records.groupby("provider_id")[column]
        .nunique(dropna=False)
    )
    conflicts = conflicts[conflicts > 1]

    if not conflicts.empty:
        raise ValueError(
            f"Conflicting {column} values for: {conflicts.index.tolist()}"
        )

# Combine unique, non-empty aliases
cleaned = (
    company_records.groupby("provider_id", as_index=False)
    .agg(
        provider_name=("provider_name", "first"),
        provider_type=("provider_type", "first"),
        country=("country", "first"),
        aliases=(
            "alias",
            lambda values: " | ".join(
                sorted(set(values.dropna().astype(str).str.strip())
                       - {""})
            )
        )
    )
)

# Add connected input count from selected companies
cleaned = cleaned.merge(
    selected[["provider_id", "connected_inputs"]],
    on="provider_id",
    how="left",
    validate="one_to_one"
)

# Check final data
# Check final data
assert cleaned["provider_id"].is_unique
assert len(cleaned) == len(selected_ids)
assert cleaned["provider_type"].eq("organization").all()

# Validate required fields separately
required_columns = [
    "provider_id",
    "provider_name",
    "provider_type",
    "country",
    "connected_inputs"
]

assert cleaned[required_columns].notnull().all().all()

# Empty aliases mean no alias is recorded in the source
cleaned["aliases"] = cleaned["aliases"].fillna("")

print("Missing required values:",
      cleaned[required_columns].isnull().sum().sum())

print("Companies without recorded aliases:",
      cleaned["aliases"].eq("").sum())

# Save
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
cleaned.to_csv(OUTPUT_FILE, index=False)

print("COMPANY DATA CLEANING COMPLETED")
print("Total companies:", len(cleaned))
print("Unique provider IDs:", cleaned["provider_id"].nunique())
print("Companies with aliases:", cleaned["aliases"].ne("").sum())
print("Missing values:\n", cleaned.isnull().sum())
print("\nCleaned company data:")
print(cleaned.to_string(index=False))
print("\nSaved to:", OUTPUT_FILE)

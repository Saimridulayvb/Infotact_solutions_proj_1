
import pandas as pd
from pathlib import Path

# File paths
input_file = Path("data/raw/providers.csv")
output_file = Path("data/processed/providers_nodes.csv")

# Load original provider data
df = pd.read_csv(input_file)

# Combine duplicate provider records
def combine_aliases(values):
    aliases = values.dropna().astype(str).str.strip()
    aliases = aliases[aliases != ""].drop_duplicates()
    return "; ".join(aliases)

providers = (
    df.groupby("provider_id", as_index=False)
    .agg(
        provider_name=("provider_name", "first"),
        provider_type=("provider_type", "first"),
        alias=("alias", combine_aliases),
        country=("country", "first")
    )
)

# Save graph-ready Provider nodes
providers.to_csv(output_file, index=False)

# Validation
print("Provider node preparation completed!")
print("Original rows:", len(df))
print("Unique Provider nodes:", len(providers))
print("Duplicate IDs remaining:", providers["provider_id"].duplicated().sum())
print("Missing provider IDs:", providers["provider_id"].isna().sum())
print("Missing aliases:", providers["alias"].eq("").sum())
print("Output file:", output_file)

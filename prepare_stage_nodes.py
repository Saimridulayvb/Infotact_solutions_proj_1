
import pandas as pd
from pathlib import Path

# File paths
input_file = Path("data/raw/stages.csv")
output_file = Path("data/processed/stages_nodes.csv")

# Load original stage records
stages = pd.read_csv(input_file)

# Validate stage identifiers
if stages["stage_id"].isna().any():
    raise ValueError("Missing stage IDs found.")

if stages["stage_id"].duplicated().any():
    raise ValueError("Duplicate stage IDs found.")

# Preserve all original columns and values
stages.to_csv(output_file, index=False)

# Validation summary
print("Stage node preparation completed!")
print("Total stages:", len(stages))
print("Unique stage IDs:", stages["stage_id"].nunique())
print("Duplicate stage IDs:", stages["stage_id"].duplicated().sum())
print("Missing stage IDs:", stages["stage_id"].isna().sum())
print("Output file:", output_file)

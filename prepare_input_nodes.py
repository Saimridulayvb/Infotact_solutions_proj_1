
import pandas as pd
from pathlib import Path

# File paths
input_file = Path("data/raw/inputs.csv")
output_file = Path("data/processed/inputs_nodes.csv")

# Load original input records
inputs = pd.read_csv(input_file)

# Validate required identifiers
if inputs["input_id"].isna().any():
    raise ValueError("Missing input IDs found.")

if inputs["input_id"].duplicated().any():
    raise ValueError("Duplicate input IDs found.")

# Preserve all original columns and values
inputs.to_csv(output_file, index=False)

# Validation summary
print("SupplyChainInput preparation completed!")
print("Total input records:", len(inputs))
print("Unique input IDs:", inputs["input_id"].nunique())
print("Duplicate input IDs:", inputs["input_id"].duplicated().sum())
print("Missing input IDs:", inputs["input_id"].isna().sum())
print("Missing stage IDs:", inputs["stage_id"].isna().sum())
print("Output file:", output_file)


import pandas as pd
from pathlib import Path

# Input and output files
raw_file = Path("data/raw/provision.csv")
providers_file = Path("data/processed/providers_nodes.csv")
inputs_file = Path("data/processed/inputs_nodes.csv")

output_file = Path("data/processed/provides_relationships.csv")
stage_records_file = Path("data/processed/provision_stage_references.csv")

# Load datasets
relationships = pd.read_csv(raw_file)
providers = pd.read_csv(providers_file)
inputs = pd.read_csv(inputs_file)

# Validate relationship endpoints
valid_provider = relationships["provider_id"].isin(
    providers["provider_id"]
)
valid_input = relationships["provided_id"].isin(
    inputs["input_id"]
)

valid_provides = relationships[valid_provider & valid_input]

# Preserve stage references separately
stage_ids = {"S1", "S2", "S3"}
stage_references = relationships[
    valid_provider & relationships["provided_id"].isin(stage_ids)
]

# Export both datasets without changing original properties
valid_provides.to_csv(output_file, index=False)
stage_references.to_csv(stage_records_file, index=False)

# Results
print("PROVIDES relationship preparation completed!")
print("Valid PROVIDES records:", len(valid_provides))
print("Stage-reference records preserved:", len(stage_references))
print("Output:", output_file)
print("Stage references:", stage_records_file)

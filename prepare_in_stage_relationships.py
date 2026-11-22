
import pandas as pd
from pathlib import Path

# Input files
inputs_file = Path("data/processed/inputs_nodes.csv")
stages_file = Path("data/processed/stages_nodes.csv")

# Output file
output_file = Path("data/processed/in_stage_relationships.csv")

# Load datasets
inputs = pd.read_csv(inputs_file)
stages = pd.read_csv(stages_file)

# Select inputs with stage information
relationships = inputs[
    inputs["stage_id"].notna()
][["input_id", "input_name", "stage_id", "stage_name"]].copy()

# Validate both endpoints
valid_input_ids = set(inputs["input_id"])
valid_stage_ids = set(stages["stage_id"])

if not relationships["input_id"].isin(valid_input_ids).all():
    raise ValueError("Invalid input IDs found.")

if not relationships["stage_id"].isin(valid_stage_ids).all():
    raise ValueError("Invalid stage IDs found.")

# Export relationship dataset
relationships.to_csv(output_file, index=False)

print("IN_STAGE preparation completed!")
print("Total IN_STAGE relationships:", len(relationships))
print("Unique input IDs:", relationships["input_id"].nunique())
print("Unique stage IDs:", relationships["stage_id"].nunique())
print("Output file:", output_file)

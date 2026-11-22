
import pandas as pd
from pathlib import Path

BASE = Path("data/processed")

# Load prepared node datasets
providers = pd.read_csv(BASE / "providers_nodes.csv")
inputs = pd.read_csv(BASE / "inputs_nodes.csv")
stages = pd.read_csv(BASE / "stages_nodes.csv")

# Load prepared relationship datasets
provides = pd.read_csv(BASE / "provides_relationships.csv")
goes_into = pd.read_csv(BASE / "goes_into_relationships.csv")
is_type_of = pd.read_csv(BASE / "is_type_of_relationships.csv")
in_stage = pd.read_csv(BASE / "in_stage_relationships.csv")

# Load separately preserved stage references
stage_references = pd.read_csv(
    BASE / "provision_stage_references.csv"
)

# Valid node IDs
provider_ids = set(providers["provider_id"])
input_ids = set(inputs["input_id"])
stage_ids = set(stages["stage_id"])

errors = []

def validate_endpoints(name, dataframe, source_column,
                       target_column, valid_sources, valid_targets):

    missing_sources = dataframe.loc[
        ~dataframe[source_column].isin(valid_sources),
        source_column
    ].dropna().unique().tolist()

    missing_targets = dataframe.loc[
        ~dataframe[target_column].isin(valid_targets),
        target_column
    ].dropna().unique().tolist()

    print(f"\n{name}")
    print("Total relationships:", len(dataframe))
    print("Missing source IDs:", missing_sources)
    print("Missing target IDs:", missing_targets)

    if missing_sources or missing_targets:
        errors.append(f"{name}: invalid endpoints found")


# Validate all four relationship types
validate_endpoints(
    "PROVIDES",
    provides,
    "provider_id",
    "provided_id",
    provider_ids,
    input_ids
)

validate_endpoints(
    "GOES_INTO",
    goes_into,
    "input_id",
    "goes_into_id",
    input_ids,
    input_ids
)

validate_endpoints(
    "IS_TYPE_OF",
    is_type_of,
    "input_id",
    "is_type_of_id",
    input_ids,
    input_ids
)

validate_endpoints(
    "IN_STAGE",
    in_stage,
    "input_id",
    "stage_id",
    input_ids,
    stage_ids
)

# Check duplicate relationship identities
duplicate_checks = {
    "PROVIDES": (provides, ["provider_id", "provided_id", "year"]),
    "GOES_INTO": (goes_into, ["input_id", "goes_into_id"]),
    "IS_TYPE_OF": (is_type_of, ["input_id", "is_type_of_id"]),
    "IN_STAGE": (in_stage, ["input_id", "stage_id"])
}

print("\nDUPLICATE RELATIONSHIP CHECK")

for name, (dataframe, columns) in duplicate_checks.items():
    count = dataframe.duplicated(subset=columns).sum()
    print(f"{name} duplicate identities:", count)

    if count > 0:
        errors.append(f"{name}: duplicate identities found")

# Verify preserved Provider-to-Stage references
print("\nPRESERVED STAGE REFERENCES")
print("Total records:", len(stage_references))
print(
    "Stage IDs found:",
    sorted(stage_references["provided_id"].dropna().unique().tolist())
)

if len(stage_references) != 21:
    errors.append("Unexpected number of preserved stage references")

# Final summary
print("\nFINAL VALIDATION SUMMARY")

if errors:
    print("Validation requires attention:")
    for error in errors:
        print("-", error)
else:
    print("All graph relationship datasets passed validation!")

print("\nTotal prepared relationships:",
      len(provides) + len(goes_into) +
      len(is_type_of) + len(in_stage))

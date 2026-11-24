
import pandas as pd
from pathlib import Path
import io
from contextlib import redirect_stdout

# ==================================================
# CONFIGURATION
# ==================================================

DATA_DIR = Path("data/processed")
REPORT_FILE = DATA_DIR / "neo4j_import_readiness_report.txt"

# Node datasets and their unique identifiers
node_datasets = {
    "Provider": ("providers_nodes.csv", "provider_id"),
    "SupplyChainInput": ("inputs_nodes.csv", "input_id"),
    "Stage": ("stages_nodes.csv", "stage_id"),
}

# Relationship datasets and endpoint mappings
relationship_datasets = {
    "PROVIDES": {
        "file": "provides_relationships.csv",
        "source": "provider_id",
        "target": "provided_id",
        "source_file": "providers_nodes.csv",
        "source_id": "provider_id",
        "target_file": "inputs_nodes.csv",
        "target_id": "input_id",
        "key": ["provider_id", "provided_id", "year"],
    },
    "GOES_INTO": {
        "file": "goes_into_relationships.csv",
        "source": "input_id",
        "target": "goes_into_id",
        "source_file": "inputs_nodes.csv",
        "source_id": "input_id",
        "target_file": "inputs_nodes.csv",
        "target_id": "input_id",
        "key": ["input_id", "goes_into_id"],
    },
    "IS_TYPE_OF": {
        "file": "is_type_of_relationships.csv",
        "source": "input_id",
        "target": "is_type_of_id",
        "source_file": "inputs_nodes.csv",
        "source_id": "input_id",
        "target_file": "inputs_nodes.csv",
        "target_id": "input_id",
        "key": ["input_id", "is_type_of_id"],
    },
    "IN_STAGE": {
        "file": "in_stage_relationships.csv",
        "source": "input_id",
        "target": "stage_id",
        "source_file": "inputs_nodes.csv",
        "source_id": "input_id",
        "target_file": "stages_nodes.csv",
        "target_id": "stage_id",
        "key": ["input_id", "stage_id"],
    },
}


# ==================================================
# NODE DATASET VALIDATION
# ==================================================

def validate_node_dataset(label, filename, id_column):

    file_path = DATA_DIR / filename

    if not file_path.exists():
        print(f"\n{label}: FILE NOT FOUND")
        return False

    df = pd.read_csv(file_path, dtype="string")

    if id_column not in df.columns:
        print(f"\n{label}: ID COLUMN NOT FOUND")
        return False

    missing_ids = df[id_column].isna().sum()
    duplicate_ids = df[id_column].duplicated().sum()

    valid = missing_ids == 0 and duplicate_ids == 0

    print(f"\n{label}")
    print(f"Total records: {len(df)}")
    print(f"Unique IDs: {df[id_column].nunique()}")
    print(f"Missing IDs: {missing_ids}")
    print(f"Duplicate IDs: {duplicate_ids}")
    print(f"Status: {'PASS' if valid else 'FAIL'}")

    return valid


# ==================================================
# RELATIONSHIP ENDPOINT VALIDATION
# ==================================================

def validate_relationship_dataset(label, config):

    file_path = DATA_DIR / config["file"]
    source_path = DATA_DIR / config["source_file"]
    target_path = DATA_DIR / config["target_file"]

    if not file_path.exists():
        print(f"\n{label}: RELATIONSHIP FILE NOT FOUND")
        return False

    if not source_path.exists() or not target_path.exists():
        print(f"\n{label}: NODE DATASET FILE NOT FOUND")
        return False

    df = pd.read_csv(file_path, dtype="string")

    required_columns = set([
        config["source"],
        config["target"],
        *config["key"],
    ])

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(f"\n{label}: MISSING COLUMNS {sorted(missing_columns)}")
        return False

    source_nodes = pd.read_csv(source_path, dtype="string")
    target_nodes = pd.read_csv(target_path, dtype="string")

    if (
        config["source_id"] not in source_nodes.columns
        or config["target_id"] not in target_nodes.columns
    ):
        print(f"\n{label}: NODE ID COLUMN NOT FOUND")
        return False

    source_ids = set(
        source_nodes[config["source_id"]].dropna()
    )

    target_ids = set(
        target_nodes[config["target_id"]].dropna()
    )

    missing_source = df[config["source"]].isna().sum()
    missing_target = df[config["target"]].isna().sum()

    invalid_source = (
        ~df[config["source"]].isin(source_ids)
    ).sum()

    invalid_target = (
        ~df[config["target"]].isin(target_ids)
    ).sum()

    duplicate_relationships = df.duplicated(
        subset=config["key"]
    ).sum()

    valid = (
        missing_source == 0
        and missing_target == 0
        and invalid_source == 0
        and invalid_target == 0
        and duplicate_relationships == 0
    )

    print(f"\n{label} RELATIONSHIPS")
    print(f"Total records: {len(df)}")
    print(f"Missing source IDs: {missing_source}")
    print(f"Missing target IDs: {missing_target}")
    print(f"Invalid source endpoints: {invalid_source}")
    print(f"Invalid target endpoints: {invalid_target}")
    print(f"Duplicate relationships: {duplicate_relationships}")
    print(f"Status: {'PASS' if valid else 'FAIL'}")

    return valid


# ==================================================
# PROVIDES RELATIONSHIP PROPERTY QUALITY ANALYSIS
# ==================================================

def validate_provides_properties():

    file_path = DATA_DIR / "provides_relationships.csv"

    print("\nPROVIDES PROPERTY QUALITY ANALYSIS")
    print("=" * 50)

    if not file_path.exists():
        print("PROVIDES dataset: FILE NOT FOUND")
        return False

    df = pd.read_csv(file_path, dtype="string")

    properties = [
        "year",
        "share_provided",
        "source",
    ]

    missing_columns = [
        column for column in properties
        if column not in df.columns
    ]

    if missing_columns:
        print(f"Missing property columns: {missing_columns}")
        return False

    print(f"Total PROVIDES records: {len(df)}")

    for column in properties:

        missing_count = int(df[column].isna().sum())
        available_count = int(df[column].notna().sum())

        missing_percentage = (
            (missing_count / len(df)) * 100
            if len(df) > 0 else 0
        )

        print(f"\nProperty: {column}")
        print(f"Available values: {available_count}")
        print(f"Missing values: {missing_count}")
        print(f"Missing percentage: {missing_percentage:.2f}%")

    # Year-specific quality analysis
    year_counts = df["year"].value_counts(dropna=False)

    print("\nYEAR-WISE RELATIONSHIP RECORDS")
    print("-" * 40)

    for year, count in year_counts.items():
        print(f"Year {year}: {count} records")

    print("\nDATA QUALITY HANDLING")
    print("Missing share values are preserved.")
    print("Missing source values are preserved.")
    print("Missing values are not replaced with zero.")

    return True


# ==================================================
# MAIN VALIDATION WORKFLOW
# ==================================================

def main():

    print("ATMOGRAPH - NEO4J IMPORT READINESS CHECK")
    print("=" * 50)

    results = []

    # Validate all node datasets
    print("\nNODE VALIDATION")

    for label, (filename, id_column) in node_datasets.items():

        result = validate_node_dataset(
            label,
            filename,
            id_column
        )

        results.append(result)

    # Validate all relationship datasets
    print("\n" + "=" * 50)
    print("RELATIONSHIP VALIDATION")

    for label, config in relationship_datasets.items():

        result = validate_relationship_dataset(
            label,
            config
        )

        results.append(result)

    # Analyse PROVIDES relationship properties
    print("\n" + "=" * 50)

    property_result = validate_provides_properties()
    results.append(property_result)

    # Final validation summary
    print("\n" + "=" * 50)
    print("FINAL VALIDATION SUMMARY")

    passed = sum(results)
    failed = len(results) - passed

    if failed == 0:
        print("ALL VALIDATION CHECKS PASSED.")
        print("Datasets are ready for Neo4j import validation.")
    else:
        print("SOME VALIDATION CHECKS FAILED.")
        print("Review the failed datasets before importing.")

    print(f"Total checks performed: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")


# ==================================================
# AUTOMATIC REPORT GENERATION
# ==================================================

if __name__ == "__main__":

    output = io.StringIO()

    with redirect_stdout(output):
        main()

    report = output.getvalue()

    # Display complete report in terminal
    print(report)

    # Save report to processed data directory
    REPORT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    REPORT_FILE.write_text(
        report,
        encoding="utf-8"
    )

    print("=" * 50)
    print(f"Report saved successfully: {REPORT_FILE}")

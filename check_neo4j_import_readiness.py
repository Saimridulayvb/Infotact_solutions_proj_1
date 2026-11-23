
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/processed")

datasets = {
    "Provider": ("providers_nodes.csv", "provider_id"),
    "SupplyChainInput": ("inputs_nodes.csv", "input_id"),
    "Stage": ("stages_nodes.csv", "stage_id"),
}

def validate_node_dataset(label, filename, id_column):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        print(f"{label}: FILE NOT FOUND")
        return False

    df = pd.read_csv(file_path)

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


def main():
    print("AT MOGRAPH - NEO4J IMPORT READINESS CHECK")
    print("=" * 45)

    results = []

    for label, (filename, id_column) in datasets.items():
        results.append(
            validate_node_dataset(label, filename, id_column)
        )

    print("\n" + "=" * 45)

    if all(results):
        print("All node datasets are ready for import validation.")
    else:
        print("Some node datasets need correction.")

    print(f"Datasets checked: {len(results)}")


if __name__ == "__main__":
    main()

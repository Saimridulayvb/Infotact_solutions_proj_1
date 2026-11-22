
import pandas as pd

datasets = {
    "Provider": {
        "file": "data/processed/providers_nodes.csv",
        "id": "provider_id",
        "columns": [
            "provider_id",
            "provider_name",
            "provider_type",
            "alias",
            "country"
        ]
    },
    "SupplyChainInput": {
        "file": "data/processed/inputs_nodes.csv",
        "id": "input_id",
        "columns": [
            "input_id",
            "input_name",
            "type",
            "stage_name",
            "stage_id",
            "description",
            "year",
            "market_share_chart_global_market_size_info",
            "market_share_chart_caption",
            "market_share_chart_source"
        ]
    },
    "Stage": {
        "file": "data/processed/stages_nodes.csv",
        "id": "stage_id",
        "columns": [
            "stage_id",
            "stage_name",
            "description",
            "market_share_chart_global_market_size_info",
            "market_share_chart_caption",
            "market_share_chart_source"
        ]
    }
}

for name, details in datasets.items():
    df = pd.read_csv(details["file"])

    missing_columns = set(details["columns"]) - set(df.columns)

    print(f"\n{name} validation")
    print("-" * 35)
    print("Records:", len(df))
    print("Unique IDs:", df[details["id"]].nunique())
    print("Duplicate IDs:", df[details["id"]].duplicated().sum())
    print("Missing IDs:", df[details["id"]].isna().sum())
    print("Missing expected columns:", missing_columns)

    if missing_columns:
        raise ValueError(f"{name} is missing required columns.")

    if df[details["id"]].isna().any():
        raise ValueError(f"{name} contains missing IDs.")

    if df[details["id"]].duplicated().any():
        raise ValueError(f"{name} contains duplicate IDs.")

print("\nAll graph node datasets passed validation!")

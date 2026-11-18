"""
AtmoGraph: Supply Chain Company Selection and Preprocessing.
Backward-compatible CLI runner using modular AtmoGraph preprocessors.
"""

import os
from pathlib import Path
from atmograph.loaders.dataset_bundle import load_dataset_bundle
from atmograph.preprocessors.pipeline import PreprocessingPipeline

def run_legacy_flow(top_n: int = 20):
    base_dir = Path(__file__).parent
    raw_dir = base_dir / "data" / "raw"
    processed_dir = base_dir / "data" / "processed"

    print("==========================================")
    print("STEP 1: LOAD CSV FILES VIA ATMOGRAPH BUNDLE")
    print("==========================================")
    bundle = load_dataset_bundle(raw_dir)
    print("CSV files loaded successfully!")
    print(f"Total raw records: {bundle.total_records}")

    print("\n--- ORGANIZATION DETAILS ---")
    orgs = bundle.providers[bundle.providers["provider_type"] == "organization"]
    print(f"Total provider records: {len(bundle.providers)}")
    print(f"Total organization records: {len(orgs)}")

    pipeline = PreprocessingPipeline(top_n=top_n)
    processed = pipeline.run_and_save(bundle, output_dir=processed_dir)

    print(f"\n--- TOP {top_n} CONNECTED COMPANIES ---")
    print(processed.selected_companies.to_string(index=False))

    print("\n--- SELECTED COMPANY SUPPLY RELATIONSHIPS (Sample) ---")
    print(processed.selected_relationships.head(10).to_string(index=False))

    print("\n========== FINAL SUMMARY ==========")
    print(f"Companies selected: {len(processed.selected_companies)}")
    print(f"Supply relationship records: {len(processed.selected_relationships)}")
    print(f"GOES_INTO relationship records: {len(processed.goes_into_relationships)}")
    print(f"IS_TYPE_OF relationship records: {len(processed.is_type_of_relationships)}")
    print("All preprocessing operations completed successfully!")

if __name__ == "__main__":
    run_legacy_flow(top_n=20)

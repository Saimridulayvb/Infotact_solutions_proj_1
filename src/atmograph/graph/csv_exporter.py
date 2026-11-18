"""
Neo4j LOAD CSV formatted dataset exporter.
"""

from pathlib import Path
from typing import Union, List
import pandas as pd

class GraphCSVExporter:
    """Exports graph nodes and edges to CSV files formatted for Neo4j LOAD CSV."""

    EXPECTED_FILES = [
        "companies_nodes.csv",
        "inputs_nodes.csv",
        "supplies_edges.csv",
        "goes_into_edges.csv",
        "is_type_of_edges.csv"
    ]

    @classmethod
    def get_expected_filenames(cls) -> List[str]:
        """Return list of standard graph CSV file basenames."""
        return list(cls.EXPECTED_FILES)

    @staticmethod
    def export(
        selected_companies_df: pd.DataFrame,
        selected_relationships_df: pd.DataFrame,
        goes_into_df: pd.DataFrame,
        is_type_of_df: pd.DataFrame,
        output_dir: Union[str, Path] = "data/processed/graph"
    ) -> Path:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        # 1. Company nodes
        comp_df = selected_companies_df[["provider_id", "provider_name", "country", "connected_inputs"]].copy()
        comp_df.columns = ["id:ID(Company)", "name", "country", "connected_inputs:int"]
        comp_df.to_csv(out_path / "companies_nodes.csv", index=False)

        # 2. Input nodes (consolidated unique)
        inputs_list = []
        seen = set()
        for _, r in selected_relationships_df.iterrows():
            iid = r["provided_id"]
            if iid not in seen:
                seen.add(iid)
                inputs_list.append({
                    "id:ID(Input)": iid,
                    "name": r.get("input_name", r.get("provided_name", iid)),
                    "type": r.get("type", "tool_resource"),
                    "stage_name": r.get("stage_name", "Fabrication")
                })
        pd.DataFrame(inputs_list).to_csv(out_path / "inputs_nodes.csv", index=False)

        # 3. Supplies relationships
        supplies_df = selected_relationships_df[["provider_id", "provided_id", "share_provided", "year"]].copy()
        supplies_df.columns = [":START_ID(Company)", ":END_ID(Input)", "share_provided:float", "year:int"]
        supplies_df.to_csv(out_path / "supplies_edges.csv", index=False)

        # 4. GoesInto relationships
        gi_df = goes_into_df[["input_id", "goes_into_id"]].copy()
        gi_df.columns = [":START_ID(Input)", ":END_ID(Input)"]
        gi_df.to_csv(out_path / "goes_into_edges.csv", index=False)

        # 5. IsTypeOf relationships
        it_df = is_type_of_df[["input_id", "is_type_of_id"]].copy()
        it_df.columns = [":START_ID(Input)", ":END_ID(Input)"]
        it_df.to_csv(out_path / "is_type_of_edges.csv", index=False)

        return out_path

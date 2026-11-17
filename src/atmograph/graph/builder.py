"""
Graph node and relationship builder from preprocessed DataFrames.
"""

from typing import List, Tuple, Set
import pandas as pd
from .models import CompanyNode, InputNode, StageNode
from .relationships import SuppliesRel, GoesIntoRel, IsTypeOfRel

class GraphBuilder:
    """Converts tabular preprocessed datasets into typed graph node and edge objects."""

    @staticmethod
    def build_companies(df: pd.DataFrame) -> List[CompanyNode]:
        nodes = []
        for _, row in df.iterrows():
            nodes.append(CompanyNode(
                id=str(row["provider_id"]),
                name=str(row["provider_name"]),
                country=str(row["country"]) if pd.notna(row.get("country")) else None,
                connected_inputs=int(row.get("connected_inputs", 0))
            ))
        return nodes

    @staticmethod
    def build_inputs(relationships_df: pd.DataFrame, goes_into_df: pd.DataFrame, is_type_df: pd.DataFrame) -> List[InputNode]:
        seen: Set[str] = set()
        nodes = []

        # From relationships
        for _, row in relationships_df.iterrows():
            iid = str(row["provided_id"])
            if iid not in seen:
                seen.add(iid)
                nodes.append(InputNode(
                    id=iid,
                    name=str(row.get("input_name", row.get("provided_name", iid))),
                    type=str(row.get("type", "unknown")),
                    stage_name=str(row.get("stage_name", "Unassigned"))
                ))

        # From sequence goes_into
        for _, row in goes_into_df.iterrows():
            for prefix in [("input_id", "input_name"), ("goes_into_id", "goes_into_name")]:
                iid = str(row[prefix[0]])
                if iid not in seen:
                    seen.add(iid)
                    nodes.append(InputNode(
                        id=iid,
                        name=str(row[prefix[1]]),
                        type="resource"
                    ))

        # From sequence is_type_of
        for _, row in is_type_df.iterrows():
            for prefix in [("input_id", "input_name"), ("is_type_of_id", "is_type_of_name")]:
                iid = str(row[prefix[0]])
                if iid not in seen:
                    seen.add(iid)
                    nodes.append(InputNode(
                        id=iid,
                        name=str(row[prefix[1]]),
                        type="resource"
                    ))

        return nodes

    @staticmethod
    def build_supplies(df: pd.DataFrame) -> List[SuppliesRel]:
        rels = []
        for _, row in df.iterrows():
            rels.append(SuppliesRel(
                from_id=str(row["provider_id"]),
                to_id=str(row["provided_id"]),
                share_provided=float(row["share_provided"]) if pd.notna(row.get("share_provided")) else None,
                year=int(row["year"]) if pd.notna(row.get("year")) else None,
                source=str(row["source"]) if pd.notna(row.get("source")) else None
            ))
        return rels

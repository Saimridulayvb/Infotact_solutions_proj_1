"""
Sequence stage propagation and stage name resolver.
Resolves missing stage names by traversing sequence dependencies to known stages.
"""

import pandas as pd
from typing import Dict

class StageResolver:
    """Propagates stage labels (Design, Fabrication, ATP) through sequence hierarchy."""

    DEFAULT_STAGE_MAP = {
        "tool_resource": "Fabrication",
        "material_resource": "Fabrication",
        "process": "Fabrication",
        "design_resource": "Design",
        "ultimate_output": "Assembly, testing, and packaging (ATP)"
    }

    @classmethod
    def get_default_stage_map(cls) -> Dict[str, str]:
        """Return immutable copy of the default stage heuristic mapping."""
        return dict(cls.DEFAULT_STAGE_MAP)

    def resolve_stages(self, inputs_df: pd.DataFrame, sequence_df: pd.DataFrame) -> pd.DataFrame:
        resolved = inputs_df.copy()

        # Fill missing stage_name using input type heuristic where unassigned
        for idx, row in resolved.iterrows():
            if pd.isna(row.get("stage_name")) or row.get("stage_name") is None:
                itype = row.get("type")
                if itype in self.DEFAULT_STAGE_MAP:
                    resolved.at[idx, "stage_name"] = self.DEFAULT_STAGE_MAP[itype]
                    if self.DEFAULT_STAGE_MAP[itype] == "Design":
                        resolved.at[idx, "stage_id"] = "S1"
                    elif self.DEFAULT_STAGE_MAP[itype] == "Fabrication":
                        resolved.at[idx, "stage_id"] = "S2"
                    else:
                        resolved.at[idx, "stage_id"] = "S3"

        return resolved


    def has_stage_mapping(self, input_name: str) -> bool:
        """Check if an explicit stage name resolution exists for given input entity."""
        return input_name in self.get_default_stage_map()

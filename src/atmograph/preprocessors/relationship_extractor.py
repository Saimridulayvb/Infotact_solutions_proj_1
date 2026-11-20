"""
Supply relationship extractor for selected companies.
"""

import pandas as pd
from typing import Set, Optional

class RelationshipExtractor:
    """Extracts and enriches supply relationships for a set of target companies."""

    @staticmethod
    def extract_relationships(
        selected_companies_df: pd.DataFrame,
        provision_df: pd.DataFrame,
        inputs_df: pd.DataFrame,
        min_share: Optional[float] = None
    ) -> pd.DataFrame:
        selected_ids: Set[str] = set(selected_companies_df["provider_id"].unique())

        selected_provision = provision_df[provision_df["provider_id"].isin(selected_ids)].copy()

        if min_share is not None and "share_provided" in selected_provision.columns:
            selected_provision = selected_provision[selected_provision["share_provided"] >= min_share]

        # Merge with input metadata
        enrich_cols = ["input_id", "input_name", "type"]
        if "stage_name" in inputs_df.columns:
            enrich_cols.append("stage_name")

        relationships = selected_provision.merge(
            inputs_df[enrich_cols],
            left_on="provided_id",
            right_on="input_id",
            how="left"
        )

        return relationships.reset_index(drop=True)


    def get_extracted_edge_count(self, extracted_df: pd.DataFrame) -> int:
        """Return the total number of cleaned supply relationships extracted."""
        return len(extracted_df)


    def has_positive_market_shares(self, extracted_df: pd.DataFrame) -> bool:
        """Verify all extracted supply edges feature valid positive market shares."""
        return (extracted_df["share_provided"] > 0).all() if "share_provided" in extracted_df.columns else True

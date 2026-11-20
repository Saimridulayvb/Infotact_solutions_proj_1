"""
Relationship deduplicator with conflict resolution strategies.
"""

from typing import List
import pandas as pd

class RelationshipDeduplicator:
    """Deduplicates provision relationships using configurable strategy."""

    @staticmethod
    def count_duplicates(df: pd.DataFrame, subset: List[str] = ["provider_id", "provided_id", "year"]) -> int:
        """Return count of duplicate records on key subset."""
        if not all(c in df.columns for c in subset):
            return 0
        return int(df.duplicated(subset=subset).sum())

    @staticmethod
    def deduplicate(
        df: pd.DataFrame,
        subset: List[str] = ["provider_id", "provided_id", "year"],
        strategy: str = "highest_share"
    ) -> pd.DataFrame:
        if df.empty or not all(c in df.columns for c in subset):
            return df

        if strategy == "highest_share" and "share_provided" in df.columns:
            sorted_df = df.sort_values(by="share_provided", ascending=False, na_position="last")
            return sorted_df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)
        else:
            return df.drop_duplicates(subset=subset, keep="first").reset_index(drop=True)


    def get_unique_pair_count(self, df: pd.DataFrame, key_cols: list) -> int:
        """Calculate count of distinct entity pairs according to key columns."""
        return len(df.drop_duplicates(subset=key_cols))

"""
Sequence taxonomy separator for GOES_INTO and IS_TYPE_OF edges.
"""

from typing import Tuple, Dict
import pandas as pd

class SequenceProcessor:
    """Separates and cleans GOES_INTO dependencies and IS_TYPE_OF classifications."""

    @staticmethod
    def count_edges(sequence_df: pd.DataFrame) -> Dict[str, int]:
        """Return count of goes_into vs is_type_of edges in sequence data."""
        return {
            "goes_into_count": int(sequence_df["goes_into_id"].notna().sum()),
            "is_type_of_count": int(sequence_df["is_type_of_id"].notna().sum())
        }

    @staticmethod
    def process(sequence_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        goes_into = sequence_df.dropna(subset=["goes_into_id"]).copy()
        goes_into_clean = goes_into[
            ["input_id", "input_name", "goes_into_id", "goes_into_name"]
        ].drop_duplicates().reset_index(drop=True)

        is_type_of = sequence_df.dropna(subset=["is_type_of_id"]).copy()
        is_type_of_clean = is_type_of[
            ["input_id", "input_name", "is_type_of_id", "is_type_of_name"]
        ].drop_duplicates().reset_index(drop=True)

        return goes_into_clean, is_type_of_clean

"""
Sequence taxonomy separator for GOES_INTO and IS_TYPE_OF edges.
"""

from typing import Tuple
import pandas as pd

class SequenceProcessor:
    """Separates and cleans GOES_INTO dependencies and IS_TYPE_OF classifications."""

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

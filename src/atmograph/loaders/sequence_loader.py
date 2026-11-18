"""
Loader for sequence dataset (GOES_INTO flow relationships and IS_TYPE_OF taxonomies).
"""

from pathlib import Path
from typing import Tuple, Union, List
import pandas as pd
from .csv_loader import CSVLoader

class SequenceLoader(CSVLoader):
    """Loader for sequence.csv defining production sequences and classification."""

    def __init__(self, file_path: Union[str, Path] = "data/raw/sequence.csv"):
        super().__init__(file_path)

    def load_goes_into(self) -> pd.DataFrame:
        df = self.load()
        goes_into = df.dropna(subset=["goes_into_id"]).copy()
        return goes_into[["input_id", "input_name", "goes_into_id", "goes_into_name"]]

    def load_is_type_of(self) -> pd.DataFrame:
        df = self.load()
        is_type_of = df.dropna(subset=["is_type_of_id"]).copy()
        return is_type_of[["input_id", "input_name", "is_type_of_id", "is_type_of_name"]]

    def get_dependency_pairs(self) -> List[Tuple[str, str]]:
        """Return raw tuples of (input_id, goes_into_id)."""
        df = self.load_goes_into()
        return list(zip(df["input_id"], df["goes_into_id"]))

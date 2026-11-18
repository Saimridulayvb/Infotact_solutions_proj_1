"""
Loader for inputs dataset (tools, materials, processes, wafers, chips).
"""

from pathlib import Path
from typing import Union, List
import pandas as pd
from .csv_loader import CSVLoader

class InputLoader(CSVLoader):
    """Loader for inputs.csv representing manufacturing nodes and dependencies."""

    EXPECTED_COLUMNS = ["input_id", "input_name", "type", "stage_name", "stage_id", "description"]

    def __init__(self, file_path: Union[str, Path] = "data/raw/inputs.csv"):
        super().__init__(file_path)

    def load_by_type(self, input_type: str) -> pd.DataFrame:
        df = self.load()
        return df[df["type"] == input_type].copy()

    def get_resource_types(self) -> List[str]:
        """Return all unique input categories present in dataset."""
        df = self.load()
        return sorted(df["type"].dropna().unique().tolist())

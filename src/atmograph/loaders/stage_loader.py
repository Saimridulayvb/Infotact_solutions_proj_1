"""
Loader for stages dataset (semiconductor manufacturing life-cycle stages).
"""

from pathlib import Path
from typing import Union, Dict
import pandas as pd
from .csv_loader import CSVLoader

class StageLoader(CSVLoader):
    """Loader for stages.csv (S1 Design, S2 Fabrication, S3 ATP)."""

    EXPECTED_COLUMNS = ["stage_id", "stage_name", "description"]

    def __init__(self, file_path: Union[str, Path] = "data/raw/stages.csv"):
        super().__init__(file_path)

    def get_stage_dict(self) -> Dict[str, str]:
        """Return dictionary mapping stage_id to stage_name."""
        df = self.load()
        return dict(zip(df["stage_id"], df["stage_name"]))

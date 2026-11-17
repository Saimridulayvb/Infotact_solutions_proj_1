"""
Loader for provision dataset (supply relationships between providers and inputs).
"""

from pathlib import Path
from typing import Union
import pandas as pd
from .csv_loader import CSVLoader

class ProvisionLoader(CSVLoader):
    """Loader for provision.csv capturing supply chain relationships and market shares."""

    EXPECTED_COLUMNS = ["provider_name", "provider_id", "provided_name", "provided_id", "share_provided", "year", "source"]

    def __init__(self, file_path: Union[str, Path] = "data/raw/provision.csv"):
        super().__init__(file_path)

    def load_clean(self) -> pd.DataFrame:
        df = self.load()
        # Convert numeric columns
        df["share_provided"] = pd.to_numeric(df["share_provided"], errors="coerce")
        df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
        return df

"""
Loader for providers dataset (organizations and countries).
"""

from pathlib import Path
from typing import Union, Optional
import pandas as pd
from .csv_loader import CSVLoader

class ProviderLoader(CSVLoader):
    """Loader for providers.csv representing entities in the semiconductor network."""

    EXPECTED_COLUMNS = ["provider_name", "alias", "provider_id", "provider_type", "country"]

    def __init__(self, file_path: Union[str, Path] = "data/raw/providers.csv"):
        super().__init__(file_path)

    def load_organizations(self) -> pd.DataFrame:
        df = self.load()
        return df[df["provider_type"] == "organization"].copy()

    def load_countries(self) -> pd.DataFrame:
        df = self.load()
        return df[df["provider_type"] == "country"].copy()

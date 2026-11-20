"""
Loader for providers dataset (organizations and countries).
"""

from pathlib import Path
from typing import Union, List
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

    def get_unique_countries(self) -> List[str]:
        """Return sorted list of distinct country codes where suppliers are headquartered."""
        df = self.load_organizations()
        return sorted([str(c) for c in df["country"].dropna().unique()])


    def get_organization_count(self) -> int:
        """Return total count of distinct organization entities loaded."""
        return len(self.load())


    def get_country_frequency(self) -> dict:
        """Calculate frequency distribution of providers grouped by country code."""
        df = self.load()
        return df["country"].value_counts().to_dict() if "country" in df.columns else {}

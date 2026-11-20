"""
Loader for provision dataset (supply relationships between providers and inputs).
"""

from pathlib import Path
from typing import Union, Optional
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

    def filter_by_year_range(self, start_year: int, end_year: int) -> pd.DataFrame:
        """Filter provisions observed within a specific calendar year range."""
        df = self.load_clean()
        return df[(df["year"] >= start_year) & (df["year"] <= end_year)].copy()


    def get_mean_market_share(self) -> float:
        """Calculate arithmetic mean of non-null market share provided values."""
        df = self.load()
        return float(df["share_provided"].dropna().mean()) if "share_provided" in df.columns else 0.0

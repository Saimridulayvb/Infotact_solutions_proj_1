"""
Generic entity filter for removing aggregate placeholders.
"""

from typing import List, Optional
import pandas as pd

class EntityFilter:
    """Filters out generic placeholder entities (e.g. 'Various companies', 'Other')."""

    DEFAULT_EXCLUSIONS = ["various companies", "other", "unknown", "multiple", "n/a"]

    def __init__(self, custom_exclusions: Optional[List[str]] = None):
        exclusions = custom_exclusions or self.DEFAULT_EXCLUSIONS
        self.stoplist = {e.lower().strip() for e in exclusions}

    def is_generic_entity(self, name: Optional[str]) -> bool:
        """Check if an individual entity name matches the generic stoplist."""
        if not name:
            return False
        return str(name).lower().strip() in self.stoplist

    def filter_providers(self, df: pd.DataFrame, col: str = "provider_name") -> pd.DataFrame:
        if col not in df.columns:
            return df
        mask = ~df[col].astype(str).str.lower().str.strip().isin(self.stoplist)
        return df[mask].copy()

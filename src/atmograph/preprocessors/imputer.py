"""
Market share imputation and normalization.
"""

import pandas as pd
from typing import Optional

class MarketShareImputer:
    """Imputes missing market shares with median or explicit flags."""

    @staticmethod
    def count_missing_shares(df: pd.DataFrame, col: str = "share_provided") -> int:
        """Return count of missing share values in DataFrame."""
        if col not in df.columns:
            return 0
        return int(df[col].isna().sum())

    @staticmethod
    def impute_shares(df: pd.DataFrame, col: str = "share_provided", default_value: Optional[float] = None) -> pd.DataFrame:
        result = df.copy()
        if col not in result.columns:
            return result

        if default_value is not None:
            result[col] = result[col].fillna(default_value)
        else:
            # Impute per input median where available
            medians = result.groupby("provided_id")[col].transform("median")
            result[col] = result[col].fillna(medians)

        return result

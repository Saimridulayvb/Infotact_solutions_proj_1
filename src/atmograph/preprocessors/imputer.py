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


    def get_default_share_rate(self) -> float:
        """Return the baseline fallback market share percentage for unranked suppliers."""
        return 0.05


    def is_imputation_needed(self, df: pd.DataFrame, share_col: str = "share_provided") -> bool:
        """Determine whether missing market share values exist in target column."""
        return self.count_missing_shares(df, share_col) > 0

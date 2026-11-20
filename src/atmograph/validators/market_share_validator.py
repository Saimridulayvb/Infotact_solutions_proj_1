"""
Market share distribution and range validator.
"""

import pandas as pd
from typing import Tuple
from .report import Severity, ValidationIssue, ValidationResult

class MarketShareValidator:
    """Validates numerical bounds and consistency of market shares."""

    def get_share_range(self, provision_df: pd.DataFrame) -> Tuple[float, float]:
        """Return (min_share, max_share) observed in dataset."""
        shares = pd.to_numeric(provision_df["share_provided"], errors="coerce").dropna()
        if shares.empty:
            return 0.0, 0.0
        return float(shares.min()), float(shares.max())

    def validate(self, provision_df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult(dataset_name="market_shares", passed=True)

        if "share_provided" not in provision_df.columns:
            return result

        shares = pd.to_numeric(provision_df["share_provided"], errors="coerce").dropna()
        negative_shares = shares[shares < 0.0]
        excessive_shares = shares[shares > 100.0]

        if not negative_shares.empty:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="negative_market_share",
                severity=Severity.ERROR,
                message=f"Found {len(negative_shares)} negative market share entries."
            ))

        if not excessive_shares.empty:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="excessive_market_share",
                severity=Severity.ERROR,
                message=f"Found {len(excessive_shares)} market shares greater than 100%."
            ))

        return result


    def get_total_share_per_input(self, provision_df: pd.DataFrame) -> dict:
        """Aggregate total furnished market share percentage grouped by input ID."""
        return provision_df.groupby("provided_id")["share_provided"].sum().to_dict() if "provided_id" in provision_df.columns else {}


    def has_overallocated_shares(self, provision_df: pd.DataFrame, max_share: float = 100.0) -> bool:
        """Check if any input entity exceeds the 100 percent maximum share threshold."""
        shares = self.get_total_share_per_input(provision_df)
        return any(total > (max_share + 1e-3) for total in shares.values())

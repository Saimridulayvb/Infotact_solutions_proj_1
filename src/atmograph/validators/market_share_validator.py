"""
Market share distribution and range validator.
"""

import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class MarketShareValidator:
    """Validates numerical bounds and consistency of market shares."""

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

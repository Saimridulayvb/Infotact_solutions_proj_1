"""
Duplicate record detector with composite key support.
"""

from typing import List, Optional
import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class DuplicateDetector:
    """Detects exact row duplicates and composite primary key violations."""

    def count_exact_duplicates(self, df: pd.DataFrame) -> int:
        """Return count of exact duplicate rows in DataFrame."""
        return int(df.duplicated().sum())

    def detect(self, dataset_name: str, df: pd.DataFrame, key_subset: Optional[List[str]] = None) -> ValidationResult:
        result = ValidationResult(dataset_name=dataset_name, passed=True)

        # Check full row duplicates
        full_dups = self.count_exact_duplicates(df)
        if full_dups > 0:
            result.issues.append(ValidationIssue(
                check_name="exact_duplicate_rows",
                severity=Severity.WARNING,
                message=f"{dataset_name} contains {full_dups} exact duplicate rows.",
                details={"duplicate_count": full_dups}
            ))

        # Check subset key duplicates
        if key_subset and all(k in df.columns for k in key_subset):
            key_dups = int(df.duplicated(subset=key_subset).sum())
            if key_dups > 0:
                result.passed = False
                result.issues.append(ValidationIssue(
                    check_name="key_duplicate_violation",
                    severity=Severity.ERROR,
                    message=f"{dataset_name} has {key_dups} duplicate records on key {key_subset}.",
                    details={"key_subset": key_subset, "duplicate_count": key_dups}
                ))

        return result

"""
Missing value detector and null threshold analyzer.
"""

from typing import Dict, Optional, List
import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class NullDetector:
    """Checks for missing values and reports critical vs warning null ratios."""

    def __init__(self, critical_threshold: float = 0.50):
        self.critical_threshold = critical_threshold

    def get_null_counts(self, df: pd.DataFrame) -> Dict[str, int]:
        """Return dictionary mapping column names to missing value counts."""
        return {col: int(df[col].isnull().sum()) for col in df.columns}

    def analyze(self, dataset_name: str, df: pd.DataFrame, non_nullable: Optional[List[str]] = None) -> ValidationResult:
        result = ValidationResult(dataset_name=dataset_name, passed=True)
        non_nullable = non_nullable or []

        total_rows = len(df)
        if total_rows == 0:
            return result

        null_counts = self.get_null_counts(df)
        for col, null_count in null_counts.items():
            null_ratio = null_count / total_rows

            if null_count > 0:
                if col in non_nullable:
                    result.passed = False
                    result.issues.append(ValidationIssue(
                        check_name="non_nullable_violation",
                        severity=Severity.ERROR,
                        message=f"Column '{col}' in {dataset_name} has {null_count} nulls but is non-nullable.",
                        details={"column": col, "null_count": null_count, "null_ratio": null_ratio}
                    ))
                elif null_ratio >= self.critical_threshold:
                    result.issues.append(ValidationIssue(
                        check_name="high_null_ratio",
                        severity=Severity.WARNING,
                        message=f"Column '{col}' has {null_ratio:.1%} missing values in {dataset_name}.",
                        details={"column": col, "null_count": null_count, "null_ratio": null_ratio}
                    ))

        return result


    def get_columns_exceeding_threshold(self, df: pd.DataFrame, threshold: float = 0.5) -> list:
        """Identify columns where null percentage exceeds the specified threshold."""
        return [c for c, ratio in (df.isnull().mean()).items() if ratio > threshold]


    def has_nulls(self, df: pd.DataFrame, column: str) -> bool:
        """Check if a specific named column contains any missing or null values."""
        return df[column].isnull().any() if column in df.columns else False

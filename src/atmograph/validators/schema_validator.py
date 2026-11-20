"""
Schema and column presence validator.
"""

from typing import Dict, List, Optional
import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class SchemaValidator:
    """Validates expected columns and basic types across datasets."""

    EXPECTED_SCHEMAS: Dict[str, List[str]] = {
        "providers": ["provider_name", "provider_id", "provider_type"],
        "provision": ["provider_name", "provider_id", "provided_name", "provided_id", "year"],
        "inputs": ["input_id", "input_name", "type"],
        "stages": ["stage_id", "stage_name"],
        "sequence": ["input_name", "input_id"]
    }

    def get_expected_columns(self, dataset_name: str) -> List[str]:
        """Return expected column list for a dataset."""
        return self.EXPECTED_SCHEMAS.get(dataset_name, [])

    def validate(self, dataset_name: str, df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult(dataset_name=dataset_name, passed=True)
        expected = self.get_expected_columns(dataset_name)

        missing_cols = [c for c in expected if c not in df.columns]
        if missing_cols:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="column_presence",
                severity=Severity.ERROR,
                message=f"Missing required columns in {dataset_name}: {missing_cols}",
                details={"missing": missing_cols}
            ))

        if df.empty:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="non_empty",
                severity=Severity.ERROR,
                message=f"Dataset {dataset_name} is empty."
            ))

        return result


    def get_missing_columns(self, df: pd.DataFrame, expected_cols: list) -> list:
        """Return list of expected column names absent in the candidate dataframe."""
        return [c for c in expected_cols if c not in df.columns]


    def has_all_columns(self, df: pd.DataFrame, expected_cols: list) -> bool:
        """Verify candidate dataframe satisfies all required column definitions."""
        return len(self.get_missing_columns(df, expected_cols)) == 0

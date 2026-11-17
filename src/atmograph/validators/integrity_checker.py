"""
Referential integrity and foreign key relationship checker.
"""

from typing import Set
import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class IntegrityChecker:
    """Verifies foreign key links between providers, provision, inputs, and stages."""

    def check_referential_integrity(
        self,
        providers_df: pd.DataFrame,
        provision_df: pd.DataFrame,
        inputs_df: pd.DataFrame,
        stages_df: pd.DataFrame
    ) -> ValidationResult:
        result = ValidationResult(dataset_name="referential_integrity", passed=True)

        valid_provider_ids: Set[str] = set(providers_df["provider_id"].dropna().astype(str))
        valid_input_ids: Set[str] = set(inputs_df["input_id"].dropna().astype(str))
        valid_stage_ids: Set[str] = set(stages_df["stage_id"].dropna().astype(str))

        # 1. Check provision provider_id -> providers.provider_id
        actual_provider_ids = set(provision_df["provider_id"].dropna().astype(str))
        orphan_providers = actual_provider_ids - valid_provider_ids
        if orphan_providers:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="orphan_provider_ids",
                severity=Severity.ERROR,
                message=f"Provision has {len(orphan_providers)} provider_ids missing from providers table.",
                details={"orphan_sample": list(orphan_providers)[:5]}
            ))

        # 2. Check provision provided_id -> inputs or stages
        actual_provided_ids = set(provision_df["provided_id"].dropna().astype(str))
        orphan_inputs = actual_provided_ids - (valid_input_ids | valid_stage_ids)
        if orphan_inputs:
            result.passed = False
            result.issues.append(ValidationIssue(
                check_name="orphan_provided_ids",
                severity=Severity.ERROR,
                message=f"Provision has {len(orphan_inputs)} provided_ids neither in inputs nor stages.",
                details={"orphan_sample": list(orphan_inputs)[:5]}
            ))

        return result

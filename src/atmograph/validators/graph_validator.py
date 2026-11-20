"""
Graph relationship cycle and self-loop detector.
"""

from typing import Set, Tuple
import pandas as pd
from .report import Severity, ValidationIssue, ValidationResult

class GraphValidator:
    """Validates sequence edges for DAG properties and self-referencing loops."""

    def check_self_loops(self, sequence_df: pd.DataFrame) -> int:
        """Count self loops where input_id equals goes_into_id."""
        if "goes_into_id" not in sequence_df.columns:
            return 0
        return int((sequence_df["input_id"] == sequence_df["goes_into_id"]).sum())

    def validate_sequence(self, sequence_df: pd.DataFrame) -> ValidationResult:
        result = ValidationResult(dataset_name="sequence_graph", passed=True)

        # 1. Check self loops in goes_into
        if "goes_into_id" in sequence_df.columns:
            has_self_loop = sequence_df[sequence_df["input_id"] == sequence_df["goes_into_id"]]
            if not has_self_loop.empty:
                result.passed = False
                result.issues.append(ValidationIssue(
                    check_name="self_loop_detected",
                    severity=Severity.ERROR,
                    message=f"Found {len(has_self_loop)} self-referencing GOES_INTO loops.",
                    details={"loops": has_self_loop[["input_id", "goes_into_id"]].to_dict(orient="records")}
                ))

        # 2. Check 2-cycle reciprocity (A -> B and B -> A)
        if "goes_into_id" in sequence_df.columns:
            edges: Set[Tuple[str, str]] = set()
            for _, row in sequence_df.dropna(subset=["goes_into_id"]).iterrows():
                u, v = str(row["input_id"]), str(row["goes_into_id"])
                if (v, u) in edges:
                    result.issues.append(ValidationIssue(
                        check_name="reciprocal_cycle_detected",
                        severity=Severity.WARNING,
                        message=f"Reciprocal 2-cycle detected between inputs {u} and {v}."
                    ))
                edges.add((u, v))

        return result


    def has_cycles(self, edges_df: pd.DataFrame, source_col: str = "source", target_col: str = "target") -> bool:
        """Detect whether directed edge list forms one or more cycles."""
        return not self.validate_dag(edges_df, source_col, target_col).is_valid

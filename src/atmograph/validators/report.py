"""
Validation report data structures and issue tracking.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional

class Severity(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class ValidationIssue:
    check_name: str
    severity: Severity
    message: str
    details: Optional[Dict[str, Any]] = None

@dataclass
class ValidationResult:
    dataset_name: str
    passed: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(i.severity in (Severity.ERROR, Severity.CRITICAL) for i in self.issues)

@dataclass
class DataQualityReport:
    results: List[ValidationResult] = field(default_factory=list)

    @property
    def total_issues(self) -> int:
        return sum(len(r.issues) for r in self.results)

    @property
    def is_valid(self) -> bool:
        return not any(r.has_errors for r in self.results)

    def summary(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "total_issues": self.total_issues,
            "datasets_checked": len(self.results),
            "error_count": sum(sum(1 for i in r.issues if i.severity in (Severity.ERROR, Severity.CRITICAL)) for r in self.results)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Export report summary as structured dictionary."""
        return self.summary()

"""
Composite data pipeline validation runner.
"""

from typing import Dict, Any
from atmograph.loaders.dataset_bundle import DatasetBundle
from .report import DataQualityReport
from .schema_validator import SchemaValidator
from .null_detector import NullDetector
from .duplicate_detector import DuplicateDetector
from .integrity_checker import IntegrityChecker
from .graph_validator import GraphValidator
from .market_share_validator import MarketShareValidator

class PipelineValidator:
    """Runs comprehensive validation suite across raw dataset bundle."""

    def __init__(self):
        self.schema_val = SchemaValidator()
        self.null_det = NullDetector()
        self.dup_det = DuplicateDetector()
        self.integrity_chk = IntegrityChecker()
        self.graph_val = GraphValidator()
        self.share_val = MarketShareValidator()

    def get_validators(self) -> Dict[str, Any]:
        """Return mapping of active sub-validator components."""
        return {
            "schema": self.schema_val,
            "null": self.null_det,
            "duplicate": self.dup_det,
            "integrity": self.integrity_chk,
            "graph": self.graph_val,
            "share": self.share_val
        }

    def run_all(self, bundle: DatasetBundle) -> DataQualityReport:
        report = DataQualityReport()

        # 1. Schemas
        report.results.append(self.schema_val.validate("providers", bundle.providers))
        report.results.append(self.schema_val.validate("provision", bundle.provision))
        report.results.append(self.schema_val.validate("inputs", bundle.inputs))
        report.results.append(self.schema_val.validate("stages", bundle.stages))
        report.results.append(self.schema_val.validate("sequence", bundle.sequence))

        # 2. Nulls on primary keys
        report.results.append(self.null_det.analyze("providers", bundle.providers, non_nullable=["provider_id"]))
        report.results.append(self.null_det.analyze("provision", bundle.provision, non_nullable=["provider_id", "provided_id"]))
        report.results.append(self.null_det.analyze("inputs", bundle.inputs, non_nullable=["input_id"]))

        # 3. Duplicates
        report.results.append(self.dup_det.detect("providers", bundle.providers, key_subset=["provider_id"]))

        # 4. Referential Integrity
        report.results.append(self.integrity_chk.check_referential_integrity(
            bundle.providers, bundle.provision, bundle.inputs, bundle.stages
        ))

        # 5. Graph checks
        report.results.append(self.graph_val.validate_sequence(bundle.sequence))

        # 6. Share checks
        report.results.append(self.share_val.validate(bundle.provision))

        return report

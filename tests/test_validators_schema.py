"""
Unit tests for schema and null detection validators.
"""

import pandas as pd
from atmograph.validators import SchemaValidator, NullDetector, Severity, DataQualityReport, ValidationResult

def test_schema_validator_valid():
    validator = SchemaValidator()
    df = pd.DataFrame({"provider_name": ["Acme"], "provider_id": ["P1"], "provider_type": ["organization"]})
    res = validator.validate("providers", df)
    assert res.passed
    assert len(res.issues) == 0

def test_schema_validator_missing_column():
    validator = SchemaValidator()
    df = pd.DataFrame({"provider_name": ["Acme"]})
    res = validator.validate("providers", df)
    assert not res.passed
    assert any(i.check_name == "column_presence" for i in res.issues)

def test_null_detector_non_nullable():
    detector = NullDetector()
    df = pd.DataFrame({"provider_id": ["P1", None], "country": ["USA", "Japan"]})
    res = detector.analyze("providers", df, non_nullable=["provider_id"])
    assert not res.passed
    assert any(i.severity == Severity.ERROR for i in res.issues)

def test_data_quality_report_to_dict():
    rep = DataQualityReport()
    rep.results.append(ValidationResult(dataset_name="test", passed=True))
    d = rep.to_dict()
    assert d["is_valid"] is True
    assert d["datasets_checked"] == 1

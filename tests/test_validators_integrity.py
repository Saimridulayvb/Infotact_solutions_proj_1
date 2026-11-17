"""
Unit tests for referential integrity, duplicate detection, and graph cycle validation.
"""

import pandas as pd
from atmograph.validators import IntegrityChecker, DuplicateDetector, GraphValidator, Severity

def test_integrity_checker_clean():
    checker = IntegrityChecker()
    providers = pd.DataFrame([{"provider_id": "P1"}])
    provision = pd.DataFrame([{"provider_id": "P1", "provided_id": "N1"}])
    inputs = pd.DataFrame([{"input_id": "N1"}])
    stages = pd.DataFrame([{"stage_id": "S1"}])

    res = checker.check_referential_integrity(providers, provision, inputs, stages)
    assert res.passed
    assert not res.has_errors

def test_duplicate_detector_subset():
    detector = DuplicateDetector()
    df = pd.DataFrame([
        {"provider_id": "P1", "provided_id": "N1", "year": 2022},
        {"provider_id": "P1", "provided_id": "N1", "year": 2022}
    ])
    res = detector.detect("provision", df, key_subset=["provider_id", "provided_id", "year"])
    assert not res.passed
    assert any(i.severity == Severity.ERROR for i in res.issues)

def test_graph_validator_no_self_loop():
    validator = GraphValidator()
    seq_df = pd.DataFrame([{"input_id": "N1", "goes_into_id": "N2"}])
    res = validator.validate_sequence(seq_df)
    assert res.passed

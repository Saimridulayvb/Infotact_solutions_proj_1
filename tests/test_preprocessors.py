"""
Unit tests for data preprocessing and cleaning components.
"""

import pandas as pd
from atmograph.preprocessors import (
    StringSanitizer,
    EntityFilter,
    RelationshipDeduplicator,
    CompanySelector,
    StageResolver,
    SequenceProcessor
)

def test_string_sanitizer():
    df = pd.DataFrame({"name": ["  Applied Materials   ", " Lam   Research  "]})
    cleaned = StringSanitizer.sanitize_dataframe(df)
    assert cleaned["name"].tolist() == ["Applied Materials", "Lam Research"]

def test_entity_filter_stoplist():
    filt = EntityFilter()
    df = pd.DataFrame({"provider_name": ["Applied Materials", "Various companies", "Other"]})
    res = filt.filter_providers(df)
    assert len(res) == 1
    assert res.iloc[0]["provider_name"] == "Applied Materials"

def test_relationship_deduplicator():
    df = pd.DataFrame([
        {"provider_id": "P1", "provided_id": "N1", "year": 2022, "share_provided": 10.0},
        {"provider_id": "P1", "provided_id": "N1", "year": 2022, "share_provided": 40.0}
    ])
    deduped = RelationshipDeduplicator.deduplicate(df)
    assert len(deduped) == 1
    assert deduped.iloc[0]["share_provided"] == 40.0

def test_stage_resolver():
    resolver = StageResolver()
    inputs = pd.DataFrame([
        {"input_id": "N8", "type": "tool_resource", "stage_name": None, "stage_id": None}
    ])
    sequence = pd.DataFrame([{"input_id": "N8", "goes_into_id": "N26"}])
    res = resolver.resolve_stages(inputs, sequence)
    assert res.iloc[0]["stage_name"] == "Fabrication"
    assert res.iloc[0]["stage_id"] == "S2"

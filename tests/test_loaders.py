"""
Unit tests for data loaders.
"""

import pytest
from pathlib import Path
from atmograph.loaders import (
    CSVLoader,
    ProviderLoader,
    ProvisionLoader,
    InputLoader,
    StageLoader,
    SequenceLoader,
    load_dataset_bundle
)

def test_csv_loader_file_not_found():
    loader = CSVLoader("non_existent_file.csv")
    with pytest.raises(FileNotFoundError):
        loader.load()

def test_load_providers(sample_data_dir: Path):
    loader = ProviderLoader(sample_data_dir / "providers.csv")
    df = loader.load()
    assert not df.empty
    assert "provider_id" in df.columns
    orgs = loader.load_organizations()
    assert (orgs["provider_type"] == "organization").all()

def test_load_provision(sample_data_dir: Path):
    loader = ProvisionLoader(sample_data_dir / "provision.csv")
    df = loader.load_clean()
    assert not df.empty
    assert "provider_id" in df.columns
    assert "share_provided" in df.columns

def test_load_sequence_splits(sample_data_dir: Path):
    loader = SequenceLoader(sample_data_dir / "sequence.csv")
    goes_into = loader.load_goes_into()
    is_type_of = loader.load_is_type_of()
    assert not goes_into.empty
    assert not is_type_of.empty
    assert "goes_into_id" in goes_into.columns
    assert "is_type_of_id" in is_type_of.columns

def test_load_dataset_bundle(sample_data_dir: Path):
    bundle = load_dataset_bundle(sample_data_dir)
    assert bundle.total_records > 0
    assert len(bundle.providers) > 0
    assert len(bundle.stages) == 3

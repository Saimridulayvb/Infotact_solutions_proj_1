"""
Pytest fixtures and configuration for AtmoGraph test suite.
"""

import pytest
from pathlib import Path
import pandas as pd

@pytest.fixture
def sample_data_dir() -> Path:
    return Path(__file__).parent.parent / "data" / "raw"

@pytest.fixture
def sample_providers_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"provider_name": "Applied Materials", "alias": "AMAT", "provider_id": "P81", "provider_type": "organization", "country": "USA"},
        {"provider_name": "Various companies", "alias": None, "provider_id": "P999", "provider_type": "organization", "country": None},
        {"provider_name": "USA", "alias": "United States", "provider_id": "P1", "provider_type": "country", "country": None}
    ])

@pytest.fixture
def sample_inputs_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"input_id": "N8", "input_name": "Crystal growing furnaces", "type": "tool_resource", "stage_name": None, "stage_id": None},
        {"input_id": "N26", "input_name": "Wafer", "type": "material_resource", "stage_name": "Fabrication", "stage_id": "S2"}
    ])

@pytest.fixture
def sample_stages_df() -> pd.DataFrame:
    return pd.DataFrame([
        {"stage_id": "S1", "stage_name": "Design", "description": "Semiconductor design"},
        {"stage_id": "S2", "stage_name": "Fabrication", "description": "Chip manufacturing"}
    ])

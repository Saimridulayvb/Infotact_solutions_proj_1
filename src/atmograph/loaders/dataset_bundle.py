"""
Unified dataset bundle aggregator for coherent access to all raw tables.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Union
import pandas as pd
from .provider_loader import ProviderLoader
from .provision_loader import ProvisionLoader
from .input_loader import InputLoader
from .stage_loader import StageLoader
from .sequence_loader import SequenceLoader

@dataclass
class DatasetBundle:
    """Container holding all raw DataFrames for the semiconductor supply chain."""
    providers: pd.DataFrame
    provision: pd.DataFrame
    inputs: pd.DataFrame
    stages: pd.DataFrame
    sequence: pd.DataFrame

    @property
    def total_records(self) -> int:
        return len(self.providers) + len(self.provision) + len(self.inputs) + len(self.stages) + len(self.sequence)

def load_dataset_bundle(data_dir: Union[str, Path] = "data/raw") -> DatasetBundle:
    """Load all 5 raw datasets from a directory."""
    base_path = Path(data_dir)
    return DatasetBundle(
        providers=ProviderLoader(base_path / "providers.csv").load(),
        provision=ProvisionLoader(base_path / "provision.csv").load_clean(),
        inputs=InputLoader(base_path / "inputs.csv").load(),
        stages=StageLoader(base_path / "stages.csv").load(),
        sequence=SequenceLoader(base_path / "sequence.csv").load()
    )

"""
Base data loader interface for AtmoGraph.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
import pandas as pd

class BaseLoader(ABC):
    """Abstract base class for all dataset loaders."""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def validate_path(self) -> None:
        """Check if the source file exists."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Dataset file does not exist: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Path is not a regular file: {self.file_path}")

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load and return the dataset as a DataFrame."""
        pass

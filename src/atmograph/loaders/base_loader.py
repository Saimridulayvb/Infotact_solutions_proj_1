"""
Base data loader interface for AtmoGraph.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union
import pandas as pd

class LoaderError(Exception):
    """Base exception for data loader failures."""
    pass

class DatasetNotFoundError(FileNotFoundError, LoaderError):
    """Raised when the expected dataset file does not exist."""
    pass

class BaseLoader(ABC):
    """Abstract base class for all dataset loaders with existence and path checks."""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    def validate_path(self) -> None:
        """Check if the source file exists and is a valid regular file."""
        if not self.file_path.exists():
            raise DatasetNotFoundError(f"Dataset file does not exist: {self.file_path}")
        if not self.file_path.is_file():
            raise LoaderError(f"Path is not a regular file: {self.file_path}")

    def get_file_size_bytes(self) -> int:
        """Return size of source dataset in bytes."""
        self.validate_path()
        return self.file_path.stat().st_size

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Load and return the dataset as a DataFrame."""
        pass

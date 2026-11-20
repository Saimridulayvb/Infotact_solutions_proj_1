"""
Resilient CSV loader with encoding detection and automatic whitespace cleaning.
"""

from pathlib import Path
from typing import List, Optional, Union, Dict
import pandas as pd
from .base_loader import BaseLoader, LoaderError

class CSVLoader(BaseLoader):
    """Resilient CSV loader supporting multiple encodings and basic sanitization."""

    SUPPORTED_ENCODINGS: List[str] = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]

    def __init__(self, file_path: Union[str, Path], dtypes: Optional[Dict] = None):
        super().__init__(file_path)
        self.dtypes = dtypes or {}

    def load(self) -> pd.DataFrame:
        self.validate_path()
        last_error = None
        for encoding in self.SUPPORTED_ENCODINGS:
            try:
                df = pd.read_csv(self.file_path, encoding=encoding, dtype=self.dtypes)
                # Strip leading/trailing whitespaces from string columns
                for col in df.select_dtypes(include="object").columns:
                    df[col] = df[col].astype(str).str.strip()
                    df[col] = df[col].replace({"nan": None, "None": None})
                return df
            except (UnicodeDecodeError, pd.errors.ParserError) as exc:
                last_error = exc
                continue

        raise LoaderError(f"Failed to load {self.file_path} with supported encodings. Last error: {last_error}")

    def read_sample(self, n_rows: int = 5) -> pd.DataFrame:
        """Quickly inspect first n rows without full table processing."""
        self.validate_path()
        return pd.read_csv(self.file_path, nrows=n_rows)


    def get_encoding(self) -> str:
        """Return the configured character encoding string for CSV parsing."""
        return self.encoding

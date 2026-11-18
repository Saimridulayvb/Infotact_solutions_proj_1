"""
String cleaning and standardization utilities.
"""

import re
from typing import Optional
import pandas as pd

class StringSanitizer:
    """Normalizes and sanitizes text columns across DataFrames."""

    @staticmethod
    def clean_text(val: Optional[str]) -> Optional[str]:
        if pd.isna(val) or val is None:
            return None
        text = str(val).strip()
        text = re.sub(r"\s+", " ", text)
        return text if text else None

    @staticmethod
    def strip_special_quotes(val: Optional[str]) -> Optional[str]:
        """Remove surrounding matched quotes from strings."""
        if not val:
            return val
        s = val.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1].strip()
        return s

    @classmethod
    def sanitize_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()
        for col in cleaned.select_dtypes(include="object").columns:
            cleaned[col] = cleaned[col].apply(cls.clean_text).apply(cls.strip_special_quotes)
        return cleaned

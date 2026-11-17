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

    @classmethod
    def sanitize_dataframe(cls, df: pd.DataFrame) -> pd.DataFrame:
        cleaned = df.copy()
        for col in cleaned.select_dtypes(include="object").columns:
            cleaned[col] = cleaned[col].apply(cls.clean_text)
        return cleaned

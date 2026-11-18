"""
Graph relationship edge models for AtmoGraph.
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class SuppliesRel:
    from_id: str  # Company ID
    to_id: str    # Input ID
    share_provided: Optional[float] = None
    year: Optional[int] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_id": self.from_id,
            "to_id": self.to_id,
            "share_provided": float(self.share_provided) if self.share_provided is not None else 0.0,
            "year": int(self.year) if self.year is not None else 0,
            "source": self.source or "Unknown"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SuppliesRel":
        return cls(
            from_id=str(data["from_id"]),
            to_id=str(data["to_id"]),
            share_provided=float(data["share_provided"]) if data.get("share_provided") is not None else None,
            year=int(data["year"]) if data.get("year") is not None else None,
            source=data.get("source")
        )

@dataclass(frozen=True)
class GoesIntoRel:
    from_id: str  # Component input ID
    to_id: str    # Target product input ID

    def to_dict(self) -> Dict[str, Any]:
        return {"from_id": self.from_id, "to_id": self.to_id}

@dataclass(frozen=True)
class IsTypeOfRel:
    from_id: str  # Subtype input ID
    to_id: str    # Parent type input ID

    def to_dict(self) -> Dict[str, Any]:
        return {"from_id": self.from_id, "to_id": self.to_id}

@dataclass(frozen=True)
class BelongsToStageRel:
    input_id: str
    stage_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {"from_id": self.input_id, "to_id": self.stage_id}

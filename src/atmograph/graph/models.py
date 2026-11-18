"""
Graph entity schemas for Neo4j nodes (Company, Input, Stage).
"""

from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class CompanyNode:
    id: str
    name: str
    country: Optional[str] = None
    connected_inputs: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country or "Unknown",
            "connected_inputs": self.connected_inputs
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompanyNode":
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            country=data.get("country"),
            connected_inputs=int(data.get("connected_inputs", 0))
        )

@dataclass(frozen=True)
class InputNode:
    id: str
    name: str
    type: str
    stage_name: Optional[str] = None
    stage_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "stage_name": self.stage_name or "Unassigned",
            "stage_id": self.stage_id or "Unassigned"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InputNode":
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            type=str(data["type"]),
            stage_name=data.get("stage_name"),
            stage_id=data.get("stage_id")
        )

@dataclass(frozen=True)
class StageNode:
    id: str
    name: str
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description or ""
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StageNode":
        return cls(
            id=str(data["id"]),
            name=str(data["name"]),
            description=data.get("description")
        )

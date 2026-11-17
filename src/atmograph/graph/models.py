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

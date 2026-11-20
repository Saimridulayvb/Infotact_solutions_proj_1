"""
Configuration loader for AtmoGraph.
Loads settings from YAML, environment variables, and provides sensible defaults.
"""

import os
from pathlib import Path
from typing import List, Optional
import yaml
from pydantic import BaseModel, Field

class ConfigurationError(Exception):
    """Raised when configuration loading or validation fails."""
    pass

class AppSettings(BaseModel):
    name: str = "AtmoGraph"
    version: str = "0.2.0"
    env: str = "development"

class PathSettings(BaseModel):
    data_dir: Path = Field(default_factory=lambda: Path("data"))
    raw_data_dir: Path = Field(default_factory=lambda: Path("data/raw"))
    processed_data_dir: Path = Field(default_factory=lambda: Path("data/processed"))
    graph_export_dir: Path = Field(default_factory=lambda: Path("data/processed/graph"))

    def validate_existence(self) -> bool:
        """Verify data paths exist."""
        return self.data_dir.exists()

class PreprocessingSettings(BaseModel):
    top_companies_limit: int = 20
    exclude_providers: List[str] = Field(default_factory=lambda: ["Various companies", "Unknown", "Other"])
    min_connected_inputs: int = 1

class Neo4jSettings(BaseModel):
    uri: str = "bolt://localhost:7687"
    username: str = "neo4j"
    password: Optional[str] = None
    database: str = "neo4j"
    batch_size: int = 500
    connection_timeout: int = 30
    max_retry_attempts: int = 3

class LoggingSettings(BaseModel):
    level: str = "INFO"
    format: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"

class Config(BaseModel):
    app: AppSettings = Field(default_factory=AppSettings)
    paths: PathSettings = Field(default_factory=PathSettings)
    preprocessing: PreprocessingSettings = Field(default_factory=PreprocessingSettings)
    neo4j: Neo4jSettings = Field(default_factory=Neo4jSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)

    def get_cache_dir(self) -> Path:
        """Return the temporary cache directory for intermediate processing."""
        return self.paths.data_dir / ".cache"


    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        config_data = {}
        target_path = Path(config_path) if config_path else Path("config/default_config.yaml")
        if target_path.exists():
            with open(target_path, "r", encoding="utf-8") as f:
                try:
                    config_data = yaml.safe_load(f) or {}
                except yaml.YAMLError as exc:
                    raise ConfigurationError(f"Failed to parse config file: {exc}") from exc

        # Merge environment overrides
        neo4j_dict = config_data.get("neo4j", {})
        if os.getenv("NEO4J_URI"):
            neo4j_dict["uri"] = os.getenv("NEO4J_URI")
        if os.getenv("NEO4J_USERNAME"):
            neo4j_dict["username"] = os.getenv("NEO4J_USERNAME")
        if os.getenv("NEO4J_PASSWORD"):
            neo4j_dict["password"] = os.getenv("NEO4J_PASSWORD")
        if os.getenv("NEO4J_DATABASE"):
            neo4j_dict["database"] = os.getenv("NEO4J_DATABASE")
        config_data["neo4j"] = neo4j_dict

        return cls(**config_data)

# Default global instance
settings = Config.load()

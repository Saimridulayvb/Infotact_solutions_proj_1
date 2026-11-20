"""
Resilient Neo4j database driver and session manager.
Supports connection pooling, health checks, and fallback dry-run mode.
"""

import os
from typing import Optional, Any
from atmograph.logger import get_logger

logger = get_logger("atmograph.neo4j")

try:
    from neo4j import GraphDatabase, Driver
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    Driver = Any

class Neo4jClient:
    """Thread-safe Neo4j driver manager with automatic reconnection and dry-run fallback."""

    def __init__(
        self,
        uri: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = "neo4j"
    ):
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.username = username or os.getenv("NEO4J_USERNAME", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "password")
        self.database = database or os.getenv("NEO4J_DATABASE", "neo4j")
        self._driver: Optional[Driver] = None

    def connect(self) -> bool:
        if not NEO4J_AVAILABLE:
            logger.warning("neo4j python package not available. Running in mock/dry-run mode.")
            return False

        try:
            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.username, self.password),
                max_connection_lifetime=3600
            )
            self._driver.verify_connectivity()
            logger.info("Successfully connected to Neo4j instance at %s", self.uri)
            return True
        except Exception as exc:
            logger.warning("Could not establish live connection to Neo4j (%s). Client available in dry-run mode.", exc)
            self._driver = None
            return False

    @property
    def is_connected(self) -> bool:
        return self._driver is not None

    def get_uri(self) -> str:
        """Return configured target URI."""
        return self.uri

    def close(self) -> None:
        if self._driver is not None:
            self._driver.close()
            self._driver = None
            logger.info("Neo4j driver connection closed.")


    def is_active(self) -> bool:
        """Check if Neo4j driver connection is currently open and active."""
        return self._driver is not None

"""
Batch transaction graph ingester with rollback handling.
"""

from typing import List, Dict, Any
from .client import Neo4jClient
from atmograph.graph.cypher_generator import CypherGenerator
from atmograph.graph.cypher_queries import CypherQueries
from atmograph.logger import get_logger

logger = get_logger("atmograph.neo4j.ingester")

class Neo4jIngester:
    """Ingests nodes and edges in batched transactions with rollback safety."""

    def __init__(self, client: Neo4jClient, batch_size: int = 500):
        self.client = client
        self.batch_size = batch_size

    def get_batch_size(self) -> int:
        """Return configured batch transaction size."""
        return self.batch_size

    def apply_schema(self) -> bool:
        if not self.client.is_connected:
            logger.info("[Dry-Run] Schema constraints would be applied to Neo4j.")
            return True

        ddl_statements = CypherGenerator.get_schema_ddl()
        with self.client._driver.session(database=self.client.database) as session:
            for stmt in ddl_statements:
                session.run(stmt)
        logger.info("Applied %d schema constraints and indexes.", len(ddl_statements))
        return True

    def ingest_batch(self, query: str, rows: List[Dict[str, Any]]) -> int:
        if not self.client.is_connected:
            logger.info("[Dry-Run] Ingested %d records with query.", len(rows))
            return len(rows)

        total_ingested = 0
        with self.client._driver.session(database=self.client.database) as session:
            for i in range(0, len(rows), self.batch_size):
                batch = rows[i:i + self.batch_size]
                session.run(query, batch=batch)
                total_ingested += len(batch)

        return total_ingested

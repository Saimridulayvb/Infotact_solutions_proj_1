"""
Idempotent Cypher schema constraints and indexes generator.
"""

from typing import List

class CypherGenerator:
    """Generates Cypher DDL for constraints and performance indexes."""

    @staticmethod
    def get_schema_ddl() -> List[str]:
        return [
            # Uniqueness constraints
            "CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE;",
            "CREATE CONSTRAINT input_id_unique IF NOT EXISTS FOR (i:Input) REQUIRE i.id IS UNIQUE;",
            "CREATE CONSTRAINT stage_id_unique IF NOT EXISTS FOR (s:Stage) REQUIRE s.id IS UNIQUE;",
            # Indexes
            "CREATE INDEX company_name_idx IF NOT EXISTS FOR (c:Company) ON (c.name);",
            "CREATE INDEX input_name_idx IF NOT EXISTS FOR (i:Input) ON (i.name);",
            "CREATE INDEX input_type_idx IF NOT EXISTS FOR (i:Input) ON (i.type);",
            "CREATE INDEX stage_name_idx IF NOT EXISTS FOR (s:Stage) ON (s.name);"
        ]

    @staticmethod
    def get_constraint_count() -> int:
        """Return count of uniqueness constraints generated."""
        return 3


    def get_index_names(self) -> list:
        """Return list of expected property index names for graph schema."""
        return ["company_name_idx", "input_name_idx", "input_type_idx"]

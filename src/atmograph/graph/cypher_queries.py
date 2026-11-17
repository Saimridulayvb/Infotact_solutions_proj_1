"""
Parameterized Cypher batch ingestion queries.
"""

class CypherQueries:
    """Cypher statements for UNWIND batch ingestion."""

    INGEST_COMPANIES = """
    UNWIND $batch AS row
    MERGE (c:Company {id: row.id})
    SET c.name = row.name,
        c.country = row.country,
        c.connected_inputs = toInteger(row.connected_inputs)
    """

    INGEST_INPUTS = """
    UNWIND $batch AS row
    MERGE (i:Input {id: row.id})
    SET i.name = row.name,
        i.type = row.type,
        i.stage_name = row.stage_name
    """

    INGEST_SUPPLIES = """
    UNWIND $batch AS row
    MATCH (c:Company {id: row.from_id})
    MATCH (i:Input {id: row.to_id})
    MERGE (c)-[r:SUPPLIES]->(i)
    SET r.share_provided = toFloat(row.share_provided),
        r.year = toInteger(row.year),
        r.source = row.source
    """

    INGEST_GOES_INTO = """
    UNWIND $batch AS row
    MATCH (a:Input {id: row.from_id})
    MATCH (b:Input {id: row.to_id})
    MERGE (a)-[:GOES_INTO]->(b)
    """

    INGEST_IS_TYPE_OF = """
    UNWIND $batch AS row
    MATCH (a:Input {id: row.from_id})
    MATCH (b:Input {id: row.to_id})
    MERGE (a)-[:IS_TYPE_OF]->(b)
    """

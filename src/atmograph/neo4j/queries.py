"""
Semiconductor supply chain ripple effect and impact analysis Cypher queries.
"""

class SupplyChainQueries:
    """Domain-specific Cypher query catalog for semiconductor disruption simulation."""

    FIND_SINGLE_POINTS_OF_FAILURE = """
    MATCH (c:Company)-[r:SUPPLIES]->(i:Input)
    WHERE r.share_provided > 70.0
    RETURN c.name AS company, c.country AS country, i.name AS critical_input, r.share_provided AS market_share
    ORDER BY market_share DESC
    """

    DOWNSTREAM_RIPPLE_EFFECT = """
    MATCH path = (c:Company {name: $company_name})-[:SUPPLIES]->(i:Input)-[:GOES_INTO*1..3]->(target:Input)
    RETURN c.name AS origin_company,
           [n in nodes(path) | n.name] AS ripple_propagation_chain,
           length(path) AS ripple_depth
    """

    STAGE_DEPENDENCY_ANALYSIS = """
    MATCH (c:Company)-[:SUPPLIES]->(i:Input)
    RETURN i.stage_name AS stage,
           count(DISTINCT c) AS supplier_count,
           count(DISTINCT i) AS input_count
    ORDER BY supplier_count DESC
    """

    GET_SUPPLIER_COUNT = """
    MATCH (c:Company)
    RETURN count(c) AS total_suppliers
    """

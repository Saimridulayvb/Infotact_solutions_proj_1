"""
Unit tests for graph modeling, Cypher generator, and NetworkX analytics.
"""

import pandas as pd
from atmograph.graph import CompanyNode, InputNode, CypherGenerator, CypherQueries, GraphAnalytics

def test_company_node():
    node = CompanyNode(id="P81", name="Applied Materials", country="USA", connected_inputs=31)
    d = node.to_dict()
    assert d["id"] == "P81"
    assert d["name"] == "Applied Materials"
    assert d["connected_inputs"] == 31

def test_cypher_generator():
    ddl = CypherGenerator.get_schema_ddl()
    assert len(ddl) > 0
    assert any("CONSTRAINT" in stmt for stmt in ddl)
    assert any("Company" in stmt for stmt in ddl)

def test_cypher_queries_defined():
    assert "UNWIND $batch" in CypherQueries.INGEST_COMPANIES
    assert "UNWIND $batch" in CypherQueries.INGEST_SUPPLIES

def test_graph_analytics():
    analytics = GraphAnalytics()
    comp_df = pd.DataFrame([{"provider_id": "P1", "provider_name": "TestCorp"}])
    rel_df = pd.DataFrame([{"provider_id": "P1", "provided_id": "N1", "input_name": "TestInput"}])
    gi_df = pd.DataFrame([{"input_id": "N1", "goes_into_id": "N2"}])

    analytics.build_from_processed(comp_df, rel_df, gi_df)
    metrics = analytics.compute_summary_metrics()
    assert metrics["node_count"] >= 2
    assert metrics["edge_count"] >= 2

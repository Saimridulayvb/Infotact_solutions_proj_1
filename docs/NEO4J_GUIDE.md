# AtmoGraph Neo4j Setup & Query Guide

This guide describes how to configure, ingest, and query the AtmoGraph semiconductor graph database.

---

## 1. Starting Neo4j Locally via Docker

```bash
docker run --name atmograph-neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -v $(pwd)/data/processed/graph:/var/lib/neo4j/import \
  neo4j:5.20-community
```

---

## 2. Setting Up Constraints & Indexes

```cypher
CREATE CONSTRAINT company_id_unique IF NOT EXISTS FOR (c:Company) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT input_id_unique IF NOT EXISTS FOR (i:Input) REQUIRE i.id IS UNIQUE;
CREATE CONSTRAINT stage_id_unique IF NOT EXISTS FOR (s:Stage) REQUIRE s.id IS UNIQUE;

CREATE INDEX company_name_idx IF NOT EXISTS FOR (c:Company) ON (c.name);
CREATE INDEX input_name_idx IF NOT EXISTS FOR (i:Input) ON (i.name);
CREATE INDEX input_type_idx IF NOT EXISTS FOR (i:Input) ON (i.type);
```

---

## 3. Disruption & Ripple Effect Cypher Queries

### Query 1: Single Points of Failure (>70% Market Share)
```cypher
MATCH (c:Company)-[r:SUPPLIES]->(i:Input)
WHERE r.share_provided > 70.0
RETURN c.name AS company, c.country AS country, i.name AS critical_input, r.share_provided AS market_share
ORDER BY market_share DESC;
```

### Query 2: Downstream Ripple Effect Simulation
```cypher
MATCH path = (c:Company {name: "Applied Materials"})-[:SUPPLIES]->(i:Input)-[:GOES_INTO*1..3]->(target:Input)
RETURN c.name AS origin_company,
       [n in nodes(path) | n.name] AS ripple_propagation_chain,
       length(path) AS ripple_depth;
```

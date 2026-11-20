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

### Query 3: Multi-Tier Upstream Supplier Tracing
```cypher
MATCH path = (origin:Input)<-[:GOES_INTO*1..3]-(comp:Input)<-[:SUPPLIES]-(supplier:Company)
WHERE origin.name = "Wafer"
RETURN supplier.name AS supplier, comp.name AS component, length(path) AS tier_depth;
```


---

## 4. Advanced Production Cypher Query Catalog & Operational Recipes

- **Recipe 01: Tier-1 Single-Source SPoF Identification** — Finds critical inputs that rely exclusively on a single supplying company with no redundant providers.
- **Recipe 02: Multi-Hop Downstream Disruption Cascades** — Traces downstream inputs affected when a specific supplier halts delivery across multiple production stages.
- **Recipe 03: Geographic Choke-Point Analysis** — Aggregates market shares of suppliers by country code to identify regional geopolitical concentration risks.
- **Recipe 04: Top-K Critical Supply Bottlenecks** — Computes bottleneck centrality by counting incoming supply edges and outgoing dependency paths.
- **Recipe 05: Raw Material Provenance Hierarchy** — Traverses upstream paths to identify all tier-3 raw chemicals and minerals feeding a final semiconductor output.
- **Recipe 06: Circular Dependency Anomaly Detection** — Checks for illegal directed cycles within the GOES_INTO relationship network to verify DAG invariants.
- **Recipe 07: Unsupplied Input Resource Audit** — Identifies input nodes that lack any incoming SUPPLIES relationship to highlight data gaps.
- **Recipe 08: Orphan Node Cleanliness Verification** — Discovers disconnected nodes having degree zero across all relationship types for database hygiene.
- **Recipe 09: High-Degree Hub Organization Ranking** — Ranks companies supplying the highest number of distinct semiconductor inputs across global fabs.
- **Recipe 10: Cross-Stage Material Transition Mapping** — Detects material flows bridging Fabrication stage inputs into Assembly, Testing, and Packaging.
- **Recipe 11: Dominant Supplier Market Share Concentration** — Flags suppliers controlling over 85 percent aggregate market share in any single semiconductor input category.
- **Recipe 12: Dual-Sourcing Redundancy Assessment** — Finds inputs supplied by exactly two companies to evaluate failover readiness and secondary supplier capacity.
- **Recipe 13: Supply Chain Depth Profiling** — Calculates maximum path length from raw precursor chemicals to completed semiconductor integrated circuits.
- **Recipe 14: Category-Level Market Share Distribution** — Groups inputs by resource type and computes average provider share percentages to benchmark competitiveness.
- **Recipe 15: Critical Photolithography Subgraph** — Isolates all suppliers, chemicals, and precision scanners connected to advanced photolithography processes.
- **Recipe 16: Silicon Wafer Dependency Subgraph** — Extracts all upstream raw quartz and downstream fabrication edges directly linked to silicon wafers.
- **Recipe 17: Packaging Substrate Upstream Tracing** — Traces chemical precursors and metal sputtering targets feeding high-density organic package substrates.
- **Recipe 18: Cleanroom Consumable Exposure Audit** — Identifies suppliers of critical gases and chemical cleaners with zero buffer stock in supply chains.
- **Recipe 19: Supplier Disruption Simulation Matrix** — Simulates simultaneous outage of top 3 suppliers and returns percentage coverage of halted manufacturing.
- **Recipe 20: Shortest Path Between Providers** — Computes shortest dependency path between any two semiconductor manufacturing firms across the supply web.
- **Recipe 21: Cross-National Sourcing Vulnerability** — Finds inputs dependent on companies in geographically contested or sanction-risk international zones.
- **Recipe 22: High-Degree Input Choke Points** — Identifies inputs that feed into more than 10 downstream manufacturing steps as high-impact nexus points.
- **Recipe 23: Stage Inflow/Outflow Balance** — Calculates ratio of incoming resources to outgoing manufactured outputs per life-cycle stage.
- **Recipe 24: Direct vs Indirect Supplier Tracing** — Compares tier-1 direct equipment providers against tier-2 indirect component manufacturers.
- **Recipe 25: Market Share Entropy Calculation** — Measures competitive balance versus monopolistic concentration across each semiconductor input market.
- **Recipe 26: APOC Weakly Connected Components** — Groups isolated subgraphs to verify overall graph connectivity using Neo4j APOC community procedures.
- **Recipe 27: APOC PageRank Node Centrality** — Calculates PageRank importance scores across all semiconductor input nodes to surface systemic importance.
- **Recipe 28: APOC Closeness Centrality Calculation** — Measures closeness centrality to find the fastest shock propagation nodes across the supply network.
- **Recipe 29: APOC Betweenness Centrality Ranking** — Discovers structural bridge entities whose removal disconnects critical supplier subgraphs.
- **Recipe 30: APOC Louvain Community Modularity** — Partitions supply network into tightly knit functional manufacturing clusters and technology domains.
- **Recipe 31: Dynamic Weight Shortest Path Traversal** — Uses Dijkstra path search with inverse market share as edge traversal impedance for risk-weighted routing.
- **Recipe 32: Out-Degree Distribution Histogram** — Aggregates supplier connectivity counts to verify scale-free graph power law properties.
- **Recipe 33: Multi-Input Bundled Supplier Analysis** — Identifies conglomerates supplying both raw materials and precision machinery to semiconductor fabs.
- **Recipe 34: Input Taxonomy Hierarchy Rollup** — Rolls up specific chemical inputs into their parent IS_TYPE_OF classification groups for executive summaries.
- **Recipe 35: Leaf Node Final Output Extraction** — Identifies terminal node products that do not feed into any further manufacturing step within the graph.
- **Recipe 36: Root Source Resource Identification** — Finds base mineral and raw chemical inputs that have no upstream dependencies in the modeled network.
- **Recipe 37: Missing Market Share Audit Query** — Flags all SUPPLIES relationships where share_provided is null or zero for data quality remediation.
- **Recipe 38: Historical Supplier Tenacity Query** — Compares multi-year provision reporting records to measure supplier persistence and partnership stability.
- **Recipe 39: Intermediate Component Fan-Out Metric** — Measures the fan-out multiplication factor from primary wafers to individual packaged micro-dies.
- **Recipe 40: Multi-Tier SPoF Propagation Warning** — Flags when a tier-1 supplier depends on a tier-2 single point of failure in their own upstream supply.
- **Recipe 41: Critical Chemical SLA Monitoring** — Audits high-purity chemical suppliers with market share above 60 percent in wafer cleaning operations.
- **Recipe 42: Tool Resource Supplier Monopolies** — Identifies proprietary machinery lines supplied by only one global vendor with high barrier to entry.
- **Recipe 43: Process Step Precursor Validation** — Checks that every process node has at least one associated tool and material input assigned.
- **Recipe 44: Downstream OEM Impact Scope Query** — Identifies final device manufacturers exposed to upstream raw wafer supply shocks and lead-time delays.
- **Recipe 45: Transitive Closure of Sub-Assemblies** — Computes full transitive closure of all sub-components inside modern 2.5D/3D packaging lines.
- **Recipe 46: Supply Edge Count Verification** — Validates total edge count against processed CSV export records for end-to-end data integrity.
- **Recipe 47: Node Label Cardinality Diagnostics** — Reports count of nodes per label (Company, Input, Stage) to verify ingestion completeness.
- **Recipe 48: Relationship Type Cardinality Check** — Returns distribution of edges across SUPPLIES, GOES_INTO, and IS_TYPE_OF relationship types.
- **Recipe 49: Self-Referencing Edge Verification** — Asserts that zero relationships have identical start and end node identifiers to prevent self-loops.
- **Recipe 50: Orphaned Edge Endpoints Diagnostic** — Confirms all relationships connect existing, non-deleted start and end nodes without broken pointers.
- **Recipe 51: High-Risk Country Export Exposure** — Sums aggregate market share across all tools supplied from high-risk jurisdiction country codes.
- **Recipe 52: Multi-Modal Transportation Node Mapping** — Identifies suppliers requiring specialized hazardous material air and maritime transport corridors.

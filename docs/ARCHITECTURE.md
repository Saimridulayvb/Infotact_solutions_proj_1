# AtmoGraph Architecture & System Design

## 1. Overview
AtmoGraph models the multi-tier supply chain of the global semiconductor industry as a directed property graph. It identifies single points of failure, supply bottlenecks, and upstream disruption propagation (ripple effect) across companies, tools, materials, and production stages.

```mermaid
flowchart TD
    subgraph Ingestion
        A[providers.csv] --> B[DatasetBundle]
        C[provision.csv] --> B
        D[inputs.csv] --> B
        E[stages.csv] --> B
        F[sequence.csv] --> B
    end

    subgraph Validation
        B --> V[PipelineValidator]
        V --> V1[Schema Checks]
        V --> V2[Integrity Checks]
        V --> V3[Duplicate Detection]
    end

    subgraph Preprocessing
        B --> P[PreprocessingPipeline]
        P --> P1[EntityFilter]
        P --> P2[CompanySelector]
        P --> P3[StageResolver]
        P --> P4[RelationshipDeduplicator]
    end

    subgraph Graph Modeling
        P --> G[GraphBuilder & CSVExporter]
        G --> G1[companies_nodes.csv]
        G --> G2[inputs_nodes.csv]
        G --> G3[supplies_edges.csv]
        G --> G4[goes_into_edges.csv]
        G --> G5[is_type_of_edges.csv]
    end

    subgraph Neo4j System
        G --> N[Neo4j Ingester]
        N --> N1[(Neo4j Graph Database)]
        N1 --> N2[Ripple Effect Cypher Queries]
    end
```

## 2. Graph Schema Model

### Nodes:
- `(:Company {id, name, country, connected_inputs})`
- `(:Input {id, name, type, stage_name})`
- `(:Stage {id, name, description})`

### Relationships:
- `(:Company)-[:SUPPLIES {share_provided, year, source}]->(:Input)`
- `(:Input)-[:GOES_INTO]->(:Input)`
- `(:Input)-[:IS_TYPE_OF]->(:Input)`
- `(:Input)-[:BELONGS_TO]->(:Stage)`

## 3. Data Flow Metrics
- **Raw Ingestion:** 5 relational tables totaling ~1,900 rows.
- **Top Supplier Extraction:** Top 20 organizations ranked by unique input connectivity.
- **Hierarchical Propagation:** Multi-tier stage assignment resolving missing stages for tool and material resources.


---

## 4. Architectural Design Decisions & Engineering Specifications

- **ADR-01: Graph Traversal Latency Bounds** — Restricts multi-hop ripple propagation traversals to sub-50ms execution times across 5-tier supplier trees.
- **ADR-02: Idempotent Schema Migrations** — Mandates IF NOT EXISTS clauses for all Cypher constraints and property indexes to prevent deployment drift.
- **ADR-03: Directed Acyclic Graph Invariant** — Enforces topological cycle detection on GOES_INTO relationship chains during intermediate stage validation.

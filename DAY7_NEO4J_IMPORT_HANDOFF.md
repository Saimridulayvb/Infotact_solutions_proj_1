
# Day 7 – AtmoGraph Neo4j Import Handoff

## 1. Objective

The objective of Day 7 is to prepare a technical handoff document for integrating the validated semiconductor supply-chain graph datasets into Neo4j.

This document provides the CSV inventory, graph structure, node and relationship mappings, uniqueness constraints, import sequence, and post-import validation requirements.

The actual Neo4j database import and integration are handled separately.

## 2. Graph Dataset Overview

The prepared graph consists of three node types and four relationship types.

### 2.1 Node datasets

| Node label | CSV file | Records | Unique identifier |
|---|---|---:|---|
| Provider | providers_nodes.csv | 396 | provider_id |
| SupplyChainInput | inputs_nodes.csv | 126 | input_id |
| Stage | stages_nodes.csv | 3 | stage_id |
| Total | | 525 | |

### 2.2 Relationship datasets

| Relationship | CSV file | Records |
|---|---|---:|
| PROVIDES | provides_relationships.csv | 1,279 |
| GOES_INTO | goes_into_relationships.csv | 52 |
| IS_TYPE_OF | is_type_of_relationships.csv | 87 |
| IN_STAGE | in_stage_relationships.csv | 11 |
| Total | | 1,429 |

All CSV headers and record counts were inspected during Day 7.

## 3. Node Schema

### 3.1 Provider

CSV: providers_nodes.csv

Properties:
- provider_id
- provider_name
- provider_type
- alias
- country

Unique identifier: provider_id

Additional labels:
- Organization: when provider_type identifies an organization.
- Country: when provider_type identifies a country.

Organization and Country are additional labels on Provider nodes, not separate node records.

### 3.2 SupplyChainInput

CSV: inputs_nodes.csv

Properties:
- input_id
- input_name
- type
- stage_name
- stage_id
- description
- year
- market_share_chart_global_market_size_info
- market_share_chart_caption
- market_share_chart_source

Unique identifier: input_id

### 3.3 Stage

CSV: stages_nodes.csv

Properties:
- stage_id
- stage_name
- description
- market_share_chart_global_market_size_info
- market_share_chart_caption
- market_share_chart_source

Unique identifier: stage_id

## 4. Relationship Schema

### 4.1 PROVIDES

Direction:

Provider → SupplyChainInput

CSV: provides_relationships.csv

Endpoint mapping:
- provider_id → Provider.provider_id
- provided_id → SupplyChainInput.input_id

Properties:
- share_provided
- year
- source

Preserve year-specific records. Missing share and source values must remain null rather than being replaced with zero or fabricated values.

### 4.2 GOES_INTO

Direction:

SupplyChainInput → SupplyChainInput

CSV: goes_into_relationships.csv

Endpoint mapping:
- input_id → source SupplyChainInput
- goes_into_id → target SupplyChainInput

### 4.3 IS_TYPE_OF

Direction:

SupplyChainInput → SupplyChainInput

CSV: is_type_of_relationships.csv

Endpoint mapping:
- input_id → source SupplyChainInput
- is_type_of_id → target SupplyChainInput

### 4.4 IN_STAGE

Direction:

SupplyChainInput → Stage

CSV: in_stage_relationships.csv

Endpoint mapping:
- input_id → SupplyChainInput.input_id
- stage_id → Stage.stage_id

Only validated stage mappings are included.

## 5. Uniqueness Constraints

Create these constraints before importing nodes:

```cypher
CREATE CONSTRAINT provider_id_unique IF NOT EXISTS
FOR (n:Provider)
REQUIRE n.provider_id IS UNIQUE;

CREATE CONSTRAINT input_id_unique IF NOT EXISTS
FOR (n:SupplyChainInput)
REQUIRE n.input_id IS UNIQUE;

CREATE CONSTRAINT stage_id_unique IF NOT EXISTS
FOR (n:Stage)
REQUIRE n.stage_id IS UNIQUE;
```

These constraints prevent duplicate graph nodes with the same identifiers.

## 6. Recommended Import Sequence

The following sequence is recommended:

1. Create uniqueness constraints.
2. Import Provider nodes.
3. Apply Organization and Country labels according to provider_type.
4. Import SupplyChainInput nodes.
5. Import Stage nodes.
6. Import PROVIDES relationships.
7. Import GOES_INTO relationships.
8. Import IS_TYPE_OF relationships.
9. Import IN_STAGE relationships.
10. Run post-import validation queries.

All nodes should exist before their relationships are created.

## 7. CSV Import Preparation

The CSV files are stored in:

data/processed/

For Neo4j LOAD CSV, the files must be made accessible through the database's configured import directory or another supported file-loading mechanism.

The exact file paths and configuration depend on the Neo4j environment.

Do not assume that the project's data/processed directory is automatically accessible to Neo4j.

## 8. Important Data Quality Findings

### 8.1 Node validation

| Dataset | Total | Unique IDs | Duplicates | Missing IDs |
|---|---:|---:|---:|---:|
| Provider | 396 | 396 | 0 | 0 |
| SupplyChainInput | 126 | 126 | 0 | 0 |
| Stage | 3 | 3 | 0 | 0 |

All three prepared node datasets passed identifier validation.

### 8.2 PROVIDES missing properties

Prepared PROVIDES records: 1,279.

- Missing share_provided: 246
- Missing source: 106
- Missing both properties: 106
- Missing share only: 140

All missing values were associated with 2019 records.

These values must not be artificially replaced during import.

### 8.3 Stage-reference records

A separate file, provision_stage_references.csv, contains 21 records.

Findings:
- All 21 records belong to 2022.
- All 21 have missing source values.
- None have missing share_provided values.
- Their provided_id values refer to Stage IDs S1, S2 and S3.

These records are excluded from PROVIDES because the agreed schema does not define a Provider-to-Stage relationship.

Do not import them as PROVIDES or invent a new relationship type without confirming the semantics.

### 8.4 Missing stage mappings

Only 11 SupplyChainInput records have validated stage mappings.

Do not assign stages to the remaining inputs without evidence.

## 9. Post-Import Validation

After importing the datasets, Member 4 should verify the node counts:

```cypher
MATCH (n:Provider)
RETURN count(n) AS provider_count;

MATCH (n:SupplyChainInput)
RETURN count(n) AS input_count;

MATCH (n:Stage)
RETURN count(n) AS stage_count;
```

Expected counts:
- Provider: 396
- SupplyChainInput: 126
- Stage: 3

Verify relationship counts:

```cypher
MATCH ()-[r:PROVIDES]->()
RETURN count(r) AS provides_count;

MATCH ()-[r:GOES_INTO]->()
RETURN count(r) AS goes_into_count;

MATCH ()-[r:IS_TYPE_OF]->()
RETURN count(r) AS is_type_of_count;

MATCH ()-[r:IN_STAGE]->()
RETURN count(r) AS in_stage_count;
```

Expected counts:
- PROVIDES: 1,279
- GOES_INTO: 52
- IS_TYPE_OF: 87
- IN_STAGE: 11

Also verify that no relationships have missing endpoints and that repeated imports do not create duplicate relationships.

## 10. Future Graph Extensions

The following labels and relationships are part of the future project scope, not the current import:

Future nodes:
- Disruption
- Location

Future relationships:
- OCCURS_AT
- AFFECTS_PROVIDER
- AFFECTS_INPUT

These can be introduced when disruption intelligence and location datasets are integrated.

## 11. Import Responsibilities

Member 1 – Data Engineering and Graph Database:
- Dataset investigation and cleaning.
- Node and relationship preparation.
- Identifier and endpoint validation.
- Data quality analysis.
- Graph schema documentation.
- Neo4j import handoff.

Member 4 – Backend and Frontend Integration:
- Neo4j database integration.
- Execution of the import process.
- Backend connectivity.
- Integration with the application.
- Post-import testing and validation.

## 12. Conclusion

The project currently contains 525 validated graph-ready node records and 1,429 validated relationship records.

The CSV datasets have been inspected, their identifiers validated, and their relationship mappings aligned with the agreed AtmoGraph graph schema.

This document provides the import reference for the next Neo4j integration stage.

The creation of this handoff document does not indicate that the Neo4j database import has already been completed.


# Day 5 – Graph Data Preparation and Validation

## 1. Objective

The objective of Day 5 was to prepare clean, schema-aligned node and relationship datasets for the AtmoGraph supply chain graph database.

The prepared datasets follow the agreed graph schema documented in GRAPH_SCHEMA.md.

## 2. Provider Node Preparation

- Source: providers.csv
- Original records: 403
- Unique Provider nodes: 396
- Duplicate provider IDs remaining: 0
- Missing provider IDs: 0

Duplicate provider IDs were investigated. The four duplicate groups had consistent provider names, types, and countries. Their unique aliases were combined instead of treating them as separate Provider nodes.

Output: data/processed/providers_nodes.csv

## 3. SupplyChainInput Node Preparation

- Source: inputs.csv
- Total records: 126
- Unique input IDs: 126
- Duplicate input IDs: 0
- Missing input IDs: 0
- Inputs with missing stage IDs: 115

Original dataset properties were preserved. Missing stage information was not guessed or artificially assigned.

Output: data/processed/inputs_nodes.csv

## 4. Stage Node Preparation

- Source: stages.csv
- Total Stage nodes: 3
- Unique stage IDs: 3
- Duplicate stage IDs: 0
- Missing stage IDs: 0

The three stages are Design, Fabrication, and Assembly, Testing, and Packaging (ATP).

Output: data/processed/stages_nodes.csv

## 5. Combined Node Validation

The prepared node datasets were checked for required columns, missing IDs, and duplicate IDs.

| Node type | Records | Unique IDs | Duplicate IDs |
|---|---:|---:|---:|
| Provider | 396 | 396 | 0 |
| SupplyChainInput | 126 | 126 | 0 |
| Stage | 3 | 3 | 0 |
| Total | 525 | 525 | 0 |

Result: All graph node datasets passed validation.

## 6. PROVIDES Relationship Preparation

- Original provision records: 1,300
- Valid PROVIDES relationships: 1,279
- Provider IDs missing from Provider nodes: 0
- Input IDs missing from SupplyChainInput nodes: 0

### Special finding: Provider-to-Stage references

A total of 21 records in provision.csv referenced S1, S2, or S3 as provided_id.

These IDs represent Stage nodes, not SupplyChainInput nodes.

Therefore:
- 1,279 valid records were prepared as PROVIDES.
- 21 Provider-to-Stage references were preserved separately.
- No unsupported relationship type was invented.

Outputs:
- data/processed/provides_relationships.csv
- data/processed/provision_stage_references.csv

## 7. GOES_INTO and IS_TYPE_OF Relationships

Existing processed relationship datasets were inspected and validated.

| Relationship | Records | Missing source IDs | Missing target IDs |
|---|---:|---:|---:|
| GOES_INTO | 52 | 0 | 0 |
| IS_TYPE_OF | 87 | 0 | 0 |

All source and target IDs were found in the prepared SupplyChainInput nodes.

## 8. IN_STAGE Relationship Preparation

Inputs with valid stage information were selected to prepare IN_STAGE relationships.

- Total IN_STAGE relationships: 11
- Unique input IDs: 11
- Unique stage IDs: 3

Only existing stage assignments were used.

Output: data/processed/in_stage_relationships.csv

## 9. Final Relationship Validation

All four relationship datasets were validated for endpoint integrity and duplicate relationship identities.

| Relationship | Records | Duplicate identities |
|---|---:|---:|
| PROVIDES | 1,279 | 0 |
| GOES_INTO | 52 | 0 |
| IS_TYPE_OF | 87 | 0 |
| IN_STAGE | 11 | 0 |
| Total | 1,429 | 0 |

Missing source IDs: 0

Missing target IDs: 0

The 21 separately preserved Provider-to-Stage references were also checked. They reference S1, S2, and S3.

Final result: All graph relationship datasets passed validation.

## 10. Scripts Created

1. prepare_provider_nodes.py
2. prepare_input_nodes.py
3. prepare_stage_nodes.py
4. validate_graph_nodes.py
5. prepare_provides_relationships.py
6. prepare_in_stage_relationships.py
7. validate_graph_relationships.py

## 11. Key Outcomes

- Prepared 525 graph-ready node records.
- Prepared 1,429 validated relationships.
- Removed duplicate Provider IDs through investigated alias consolidation.
- Validated relationship endpoints against the prepared node datasets.
- Preserved the 21 Provider-to-Stage references separately.
- Preserved missing source values rather than inventing data.
- Followed the agreed AtmoGraph graph schema.

## 12. Current Implementation Status

Node and relationship CSV preparation and validation are complete.

The datasets are ready to be used by the Neo4j integration workflow.

Neo4j import and database-level verification are not claimed as completed in this work.

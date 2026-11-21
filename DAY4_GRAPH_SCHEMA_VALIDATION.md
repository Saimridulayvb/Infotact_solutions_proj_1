
# Day 4 – AtmoGraph Graph Schema Validation

## 1. Objective

Validate the agreed Neo4j graph schema against the five raw semiconductor supply-chain datasets before graph construction.

## 2. Datasets Validated

| Dataset | Records | Graph Component |
|---|---:|---|
| providers.csv | 403 | Provider, Organization, Country |
| inputs.csv | 126 | SupplyChainInput |
| stages.csv | 3 | Stage |
| provision.csv | 1,300 | PROVIDES |
| sequence.csv | 139 | GOES_INTO, IS_TYPE_OF |

## 3. Validation Findings

### 3.1 Provider Validation
- 403 provider records.
- 380 organization records.
- 23 country records.
- All five CSV columns match the proposed Provider properties.

### 3.2 SupplyChainInput Validation
- 126 input records.
- All 10 CSV columns are represented in the proposed schema.
- 115 records have missing stage_id and stage_name.
- Missing stage information will not be invented.

### 3.3 Stage Validation
- 3 unique stage records: Design (S1), Fabrication (S2), and Assembly, testing, and packaging (S3).
- No missing stage IDs or names.
- One missing market-share information value.
- IN_STAGE relationships will only be created for valid stage IDs.

### 3.4 PROVIDES Relationship Validation
- 1,300 raw supply records.
- 302 unique providers.
- 113 unique provided input IDs.
- 246 missing share_provided values.
- 127 missing source values.
- No missing provider or provided IDs.
- Year information is available for all records.

### 3.5 Sequence Relationship Validation
- 139 records.
- 52 GOES_INTO relationships.
- 87 IS_TYPE_OF relationships.
- Missing relationship columns are expected because the two relationship types are stored separately.

## 4. ID Validation

Compared sequence.csv identifiers against inputs.csv.

| Validation | Missing IDs |
|---|---:|
| Source input IDs | 0 |
| GOES_INTO target IDs | 0 |
| IS_TYPE_OF target IDs | 0 |

All referenced input IDs exist in inputs.csv.

## 5. Graph Construction Rules

- Preserve source IDs and values.
- Do not replace missing shares with zero.
- Do not invent missing stage assignments.
- Create relationships only when both endpoint nodes exist.
- Preserve the direction of GOES_INTO and IS_TYPE_OF.
- Preserve year and source properties on PROVIDES relationships.
- Do not import raw and processed versions of the same relationships together.
- Validate country matching before creating BASED_IN relationships.

## 6. Validation Conclusion

All five raw datasets have been inspected and their core columns and relationship mappings are supported by the proposed graph schema.

The input identifiers used by sequence.csv have also been validated against inputs.csv.

The schema is ready to proceed to graph construction, subject to the documented missing-value rules and final coordination with Member 4.

This validation confirms dataset compatibility. It does not claim that the Neo4j graph has already been implemented or tested.

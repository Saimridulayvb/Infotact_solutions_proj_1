
# Day 6 – Relationship Data Quality and Preservation Analysis

## 1. Objective

The objective of Day 6 was to inspect the prepared relationship datasets, analyse missing relationship properties, and verify that the data preparation process preserved the original source values.

## 2. Relationship Dataset Inspection

Four prepared relationship datasets were inspected.

| Relationship | Records | Missing values |
|---|---:|---:|
| PROVIDES | 1,279 | Optional properties missing |
| GOES_INTO | 52 | 0 |
| IS_TYPE_OF | 87 | 0 |
| IN_STAGE | 11 | 0 |

All datasets contained the expected relationship columns.

## 3. PROVIDES Property Analysis

The PROVIDES relationship contains the following properties:

- provider_name
- provider_id
- provided_name
- provided_id
- share_provided
- year
- source

Missing-value analysis:

| Property | Missing records |
|---|---:|
| share_provided | 246 |
| source | 106 |

All required endpoint identifiers and year values were populated.

## 4. Missing Values by Year

| Year | Missing share_provided | Missing source |
|---|---:|---:|
| 2019 | 246 | 106 |
| 2021 | 0 | 0 |
| 2022 | 0 | 0 |
| 2025 | 0 | 0 |

The missing values were concentrated in the 2019 records.

## 5. Detailed 2019 Analysis

The prepared PROVIDES dataset contained 264 records from 2019.

The records represented 21 different supplied product or service categories, including:

- Electronic gases
- Ceramic packages
- CMP materials
- Electronic design automation software
- Wafer
- Photoresists
- Photomasks
- Core intellectual property
- Wet chemicals
- Substrates

Missing-value distribution:

- 106 records had both share_provided and source missing.
- 140 records had only share_provided missing.
- 0 records had only source missing.

Missing values were preserved without assigning artificial values.

## 6. Raw and Prepared Dataset Comparison

The 2019 records were compared between raw provision.csv and prepared provides_relationships.csv.

| Check | Raw | Prepared |
|---|---:|---:|
| 2019 records | 264 | 264 |
| Missing share_provided | 246 | 246 |
| Missing source | 106 | 106 |
| Unique provider IDs | 157 | 157 |

The matching counts confirm that the preparation process preserved the 2019 records and their missing-value patterns.

## 7. Investigation of the 21 Stage References

The raw provision dataset contained 1,300 records, while the prepared PROVIDES dataset contained 1,279 records.

The remaining 21 records were preserved separately in provision_stage_references.csv.

Investigation confirmed:

- Total stage-reference records: 21
- Year: 2022
- Missing source values: 21
- Missing share_provided values: 0
- Referenced Stage IDs: S1, S2, S3

These records refer to Stage nodes rather than SupplyChainInput nodes.

They were therefore kept separate instead of being incorrectly represented as PROVIDES relationships.

This explains the difference between the raw source missing count (127) and the prepared PROVIDES missing count (106).

## 8. Neo4j Import Considerations

The following data-handling rules were identified:

1. Preserve missing share_provided values as null.
2. Preserve missing source values as null.
3. Retain year-specific relationship information.
4. Do not replace missing values with zero or fabricated text.
5. Import only validated Provider-to-SupplyChainInput records as PROVIDES.
6. Keep the 21 Provider-to-Stage references separate until their relationship semantics are clarified.

## 9. Conclusion

The Day 6 analysis confirmed that the prepared relationship datasets preserve the original data values for retained records.

The missing-value patterns were investigated and explained, including the difference between the raw and prepared source counts.

The prepared relationship datasets remain suitable for the next Neo4j integration stage, subject to the agreed relationship mapping and import validation.

No Neo4j import is claimed as completed in this analysis.


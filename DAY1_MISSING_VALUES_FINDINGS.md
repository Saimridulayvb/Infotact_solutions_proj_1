
# AtmoGraph – Day 1 Missing Values Investigation

## Objective
Investigate missing values in the semiconductor supply-chain dataset before cleaning.

## Dataset overview
- Providers: 403 records
- Inputs: 126 records
- Provision: 1300 records
- Sequence: 139 records
- Stages: 3 records

## Processed dataset
- Selected companies: 20
- Selected company-input relationships: 254
- GOES_INTO relationships: 52
- IS_TYPE_OF relationships: 87

## Key findings
1. Provider aliases are missing in 330 records.
2. Country is missing in 22 country-type records.
3. Only 11 input records have stage information.
4. Six selected relationships have missing share_provided.
5. Four selected relationships have missing source.
6. All 254 selected relationships have missing stage_name.

## Cleaning decisions
- Preserve unavailable aliases and sources.
- Do not replace missing share values with zero.
- Do not assign production stages without supporting data.
- Keep GOES_INTO and IS_TYPE_OF relationships separate.
- Preserve original raw CSV files.

## Conclusion
The missing values were investigated. No original dataset values
were modified. Further cleaning and validation will be performed
in the next stage.

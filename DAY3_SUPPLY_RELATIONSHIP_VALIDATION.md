
# Day 3 – Supply Relationship Validation

## Objective
Validate company-to-input supply relationships before graph construction.

## Dataset
data/processed/selected_relationships.csv

## Dataset Overview
- Total relationships: 254
- Unique providers: 20
- Unique inputs: 76
- Tool resources: 248
- Material resources: 6

## Validation Performed

### 1. Provider ID Validation
All provider IDs were matched against cleaned_companies.csv.
Invalid provider IDs: 0

### 2. Input ID Validation
All provided_id values were matched against inputs.csv.
Invalid input IDs: 0

### 3. Name Consistency
- Company name mismatches: 0
- Input name mismatches: 0

### 4. Duplicate Relationship Validation
Checked using provider_id, provided_id and year.
Duplicate relationships: 0

### 5. Missing Values
- share_provided: 6
- source: 4
- stage_name: 254

The six missing share values belong to material-resource
relationships from 2019. Missing values were preserved.

All selected relationships have missing stage_name.
No unsupported stage assignments were made.

### 6. Year Distribution
- 2025: 248 relationships
- 2019: 6 relationships

### 7. Supply Share Validation
- Available values: 248
- Minimum: 1.1
- Maximum: 100.0
- Mean: 22.05
- Negative values: 0
- Values above 100: 0

## Output
- validate_supply_relationships.py
- data/processed/supply_relationship_validation_report.txt

## Conclusion
The 254 selected supply relationships passed the ID,
name-consistency and duplicate checks. Missing values
were investigated and preserved without unsupported
imputation. The dataset is ready for the next stage
of graph schema finalisation, subject to team schema
agreement.


# Day 2 – Company Data Cleaning and Validation

## Objective
Clean and validate the selected semiconductor supply-chain company records before graph construction.

## Dataset Used
- Raw dataset: providers.csv
- Selected dataset: selected_companies.csv

## Investigation
- Selected 20 companies for the project.
- Checked provider IDs against the original provider dataset.
- Identified 4 provider IDs with repeated records.
- Confirmed that repeated records had consistent company names, provider types, and countries.
- Identified aliases associated with 8 selected companies.

## Cleaning Performed
- Retained one record per unique provider ID.
- Combined unique aliases into a single field.
- Preserved provider name, provider type, and country.
- Retained connected_inputs from the selected company dataset.
- Kept the original raw dataset unchanged.
- Represented companies without recorded aliases using empty strings.

## Validation Results
- Total company records: 20
- Unique provider IDs: 20
- Duplicate provider IDs: 0
- Missing required values: 0
- Companies with aliases: 8
- Companies without recorded aliases: 12

## Output Files
- clean_company_data.py
- data/processed/cleaned_companies.csv

## Conclusion
Company data cleaning and validation were completed successfully.
The cleaned dataset contains 20 unique company records and is ready
for the next stage of supply-chain relationship validation.

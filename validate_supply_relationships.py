
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. LOAD DATASETS
# --------------------------------------------------

relationship_file = Path("data/processed/selected_relationships.csv")
company_file = Path("data/processed/cleaned_companies.csv")
input_file = Path("data/raw/inputs.csv")

relationships = pd.read_csv(relationship_file)
companies = pd.read_csv(company_file)
inputs = pd.read_csv(input_file)

print("DATASETS LOADED SUCCESSFULLY")

# --------------------------------------------------
# 2. VALIDATE PROVIDER IDS
# --------------------------------------------------

invalid_providers = relationships[
    ~relationships["provider_id"].isin(companies["provider_id"])
]

# --------------------------------------------------
# 3. VALIDATE INPUT IDS
# --------------------------------------------------

invalid_inputs = relationships[
    ~relationships["provided_id"].isin(inputs["input_id"])
]

# Check whether provided_id and input_id match
id_mismatches = relationships[
    relationships["provided_id"] != relationships["input_id"]
]

# --------------------------------------------------
# 4. VALIDATE COMPANY NAMES
# --------------------------------------------------

company_lookup = companies.set_index("provider_id")["provider_name"]

expected_company_names = relationships["provider_id"].map(company_lookup)

company_name_mismatches = relationships[
    relationships["provider_name"].str.strip()
    != expected_company_names.str.strip()
]

# --------------------------------------------------
# 5. VALIDATE INPUT NAMES
# --------------------------------------------------

input_lookup = inputs.set_index("input_id")["input_name"]

expected_input_names = relationships["provided_id"].map(input_lookup)

input_name_mismatches = relationships[
    relationships["provided_name"].str.strip()
    != expected_input_names.str.strip()
]

# --------------------------------------------------
# 6. CHECK DUPLICATE RELATIONSHIPS
# --------------------------------------------------

duplicate_relationships = relationships[
    relationships.duplicated(
        subset=["provider_id", "provided_id", "year"],
        keep=False
    )
]

# --------------------------------------------------
# 7. CHECK MISSING VALUES
# --------------------------------------------------

missing_values = relationships.isnull().sum()

missing_share = relationships["share_provided"].isnull().sum()
missing_source = relationships["source"].isnull().sum()
missing_stage = relationships["stage_name"].isnull().sum()

# --------------------------------------------------
# 8. CHECK INPUT TYPES AND YEARS
# --------------------------------------------------

input_type_counts = relationships["type"].value_counts()

year_counts = relationships["year"].value_counts(dropna=False)

# --------------------------------------------------
# 9. GENERATE VALIDATION REPORT
# --------------------------------------------------

report = f"""
SUPPLY RELATIONSHIP VALIDATION REPORT
=====================================

Total relationships: {len(relationships)}

Unique providers: {relationships['provider_id'].nunique()}

Unique inputs: {relationships['provided_id'].nunique()}

PROVIDER ID VALIDATION
---------------------
Provider IDs not found: {invalid_providers['provider_id'].nunique()}

INPUT ID VALIDATION
-------------------
Input IDs not found: {invalid_inputs['provided_id'].nunique()}

Provided ID and input ID mismatches: {len(id_mismatches)}

COMPANY NAME VALIDATION
-----------------------
Company name mismatches: {len(company_name_mismatches)}

INPUT NAME VALIDATION
---------------------
Input name mismatches: {len(input_name_mismatches)}

DUPLICATE VALIDATION
--------------------
Duplicate relationship rows: {len(duplicate_relationships)}

MISSING VALUES
--------------
Missing share_provided: {missing_share}

Missing source: {missing_source}

Missing stage_name: {missing_stage}

INPUT TYPE DISTRIBUTION
-----------------------
{input_type_counts.to_string()}

YEAR DISTRIBUTION
-----------------
{year_counts.to_string()}

OVERALL RESULT
--------------
Provider IDs valid: {len(invalid_providers) == 0}
Input IDs valid: {len(invalid_inputs) == 0}
No duplicate relationships: {len(duplicate_relationships) == 0}
Company names consistent: {len(company_name_mismatches) == 0}
Input names consistent: {len(input_name_mismatches) == 0}
"""

# --------------------------------------------------
# 10. SAVE REPORT
# --------------------------------------------------

output_file = Path(
    "data/processed/supply_relationship_validation_report.txt"
)

output_file.write_text(report, encoding="utf-8")

print(report)

print("REPORT SAVED TO:", output_file)

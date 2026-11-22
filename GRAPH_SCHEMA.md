# AtmoGraph – Project Graph Schema

## 1. Purpose

This document defines the agreed Neo4j graph schema for AtmoGraph's semiconductor supply-chain data.

The core graph represents:
- Providers supplying semiconductor inputs.
- Dependencies between supply-chain inputs.
- Manufacturing stages associated with inputs.

Disruption modelling will be added later when verified disruption and location datasets are available.

## 2. Node Labels and Properties

### 2.1 Provider

Represents provider records from `providers.csv`.

Properties:
- `provider_id` – unique identifier
- `provider_name` – provider name
- `provider_type` – organization or country
- `alias` – alternative provider names, when available
- `country` – associated country, when available

**Uniqueness:** `provider_id`

### 2.2 Organization

An additional label on Provider nodes where `provider_type = organization`.

Uses the same properties as Provider.

### 2.3 Country

An additional label on Provider nodes where `provider_type = country`.

Uses the same provider properties. Do not invent country codes or country names that are not supported by the source data.

### 2.4 SupplyChainInput

Represents semiconductor inputs from `inputs.csv`.

Properties:
- `input_id` – unique identifier
- `input_name` – input name
- `type` – input category
- `stage_name`
- `stage_id`
- `description`
- `year`
- `market_share_chart_global_market_size_info`
- `market_share_chart_caption`
- `market_share_chart_source`

Preserve source values and handle missing values without inventing information.

**Uniqueness:** `input_id`

### 2.5 Stage

Represents manufacturing stages from `stages.csv`.

Properties:
- `stage_id` – unique identifier
- `stage_name`
- `description`
- Market metadata fields, when available

**Uniqueness:** `stage_id`

### 2.6 Future Nodes

The following nodes are planned for future disruption modelling.

**Disruption**
- `event_id`
- `event_type`
- `name`
- `severity`
- `start_time`
- `end_time`
- `status`
- `source`

**Location**
- `location_id`
- `name`
- `country_code`
- `location_type`
- `latitude`
- `longitude`

These nodes require verified event and location data.

## 3. Relationship Types and Directions

| Relationship | Direction | Source |
|---|---|---|
| PROVIDES | Provider → SupplyChainInput | provision.csv |
| GOES_INTO | SupplyChainInput → SupplyChainInput | sequence.csv |
| IS_TYPE_OF | SupplyChainInput → SupplyChainInput | sequence.csv |
| IN_STAGE | SupplyChainInput → Stage | inputs.csv |
| BASED_IN | Organization → Country | Validated country matching |

### 3.1 PROVIDES

Properties:
- `share_provided`
- `year`
- `source`

Mapping:
- `provider_id` identifies the Provider.
- `provided_id` identifies the SupplyChainInput.

Preserve separate year-specific supply records. Do not use null values inside a Neo4j MERGE pattern. Records with missing years require a separately defined identity and loading strategy.

### 3.2 GOES_INTO

Direction:

`SupplyChainInput(input_id) → SupplyChainInput(goes_into_id)`

Preserve the direction recorded in `sequence.csv`.

### 3.3 IS_TYPE_OF

Direction:

`SupplyChainInput(input_id) → SupplyChainInput(is_type_of_id)`

Preserve the direction recorded in `sequence.csv`.

### 3.4 IN_STAGE

Direction:

`SupplyChainInput → Stage`

Create this relationship only when `stage_id` is present and matches a valid Stage node.

### 3.5 BASED_IN

Direction:

`Organization → Country`

Create only after validating country matching and confirming the meaning of the source country field.

## 4. Future Relationships

These relationships require verified disruption data:

- `OCCURS_AT`: Disruption → Location
- `AFFECTS_PROVIDER`: Disruption → Provider
- `AFFECTS_INPUT`: Disruption → SupplyChainInput

Do not create synthetic events or unsupported impact relationships.

## 5. CSV-to-Graph Mapping

| CSV file | Graph operation |
|---|---|
| providers.csv | Create Provider nodes and add Organization or Country labels |
| inputs.csv | Create SupplyChainInput nodes |
| stages.csv | Create Stage nodes |
| provision.csv | Create PROVIDES relationships |
| sequence.csv | Create GOES_INTO and IS_TYPE_OF relationships |
| selected_companies.csv | Optional selection metadata on matching Provider nodes |
| selected_relationships.csv | Optional filtered PROVIDES relationships |
| goes_into_relationships.csv | Optional validated GOES_INTO subset |
| is_type_of_relationships.csv | Optional validated IS_TYPE_OF subset |

**Import rule:** Use either the original relationship CSVs or their processed subsets for a given import run. Do not import both indiscriminately.

## 6. Uniqueness Constraints

Apply these constraints before importing graph data:

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

Organization and Country labels reuse Provider identity.

## 7. Data Validation and Missing-Value Rules

- Validate provider IDs before creating PROVIDES relationships.
- Validate input IDs before creating input-to-input relationships.
- Preserve original source values.
- Do not replace missing shares with zero.
- Do not assign manufacturing stages without source evidence.
- Do not create relationships when their required endpoint cannot be matched.
- Handle missing relationship years separately from year-specific records.
- Preserve source and year information for PROVIDES relationships.

## 8. Implementation Scope

### Core milestone
- Provider
- Organization
- Country
- SupplyChainInput
- Stage
- PROVIDES
- GOES_INTO
- IS_TYPE_OF
- IN_STAGE
- Conditional BASED_IN

### Future milestone
- Disruption
- Location
- OCCURS_AT
- AFFECTS_PROVIDER
- AFFECTS_INPUT

### Prediction milestone
- Time-aware graph snapshots
- Graph features
- Verified impact labels
- Graph Neural Network-based impact prediction

## 9. Implementation Status and Limitations

This document defines the agreed target schema. It does not claim that the schema or its relationships have already been implemented in Neo4j.

Implementation and testing will be documented separately.
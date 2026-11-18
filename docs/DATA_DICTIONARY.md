# AtmoGraph Data Dictionary

This document details all raw and processed datasets modeled in the AtmoGraph semiconductor supply chain knowledge graph.

---

## 1. Raw Datasets (`data/raw/`)

### 1.1 `providers.csv`
Represents manufacturing and supplier entities within the global semiconductor ecosystem.
- `provider_name` (string): Primary business name (e.g. *Applied Materials*, *ASML*, *TSMC*).
- `alias` (string, nullable): Alternative legal, operating, or regional name.
- `provider_id` (string, PK): Unique entity identifier (e.g. `P81`, `P111`).
- `provider_type` (string): Entity classification (`organization` or `country`).
- `country` (string, nullable): Three-letter ISO alpha-3 country code where headquartered.

### 1.2 `provision.csv`
Captures supply and capability relationships where a provider furnishes an input or participates in a stage.
- `provider_name` (string): Name of the supplying organization or nation.
- `provider_id` (string, FK $\rightarrow$ `providers.provider_id`): Provider identifier.
- `provided_name` (string): Name of the semiconductor input or life-cycle stage provided.
- `provided_id` (string, FK $\rightarrow$ `inputs.input_id` / `stages.stage_id`): Target entity ID.
- `share_provided` (float, nullable): Market share percentage ($0.0 - 100.0\%$).
- `year` (integer): Reporting or observation year.
- `source` (string, nullable): Attribution citation.

### 1.3 `inputs.csv`
Semiconductor manufacturing resources, machines, materials, processes, and outputs.
- `input_id` (string, PK): Unique identifier (e.g. `N8`, `N26`).
- `input_name` (string): Canonical name (e.g. *Crystal growing furnaces*, *Wafer*).
- `type` (string): Categorical type (`tool_resource`, `material_resource`, `process`, `design_resource`, `ultimate_output`).
- `stage_name` (string, nullable): Life-cycle stage (*Design*, *Fabrication*, *ATP*).
- `stage_id` (string, nullable): Life-cycle stage ID (`S1`, `S2`, `S3`).
- `description` (string): Technical explanation of function.

### 1.4 `stages.csv`
High-level semiconductor life-cycle segments.
- `stage_id` (string, PK): `S1`, `S2`, `S3`.
- `stage_name` (string): *Design*, *Fabrication*, *Assembly, testing, and packaging (ATP)*.
- `description` (string): Life-cycle scope and overview.

### 1.5 `sequence.csv`
Dependency hierarchy and taxonomy relationships between inputs.
- `input_name` / `input_id`: Upstream source input.
- `goes_into_name` / `goes_into_id`: Target input consumed or assembled into.
- `is_type_of_name` / `is_type_of_id`: Taxonomic parent classification.

---

## 2. Processed Datasets (`data/processed/`)

- `selected_companies.csv`: Top 20 organizations ranked by connected unique input count.
- `selected_relationships.csv`: Cleaned, deduplicated supply edges for the selected companies with stage metadata.
- `goes_into_relationships.csv`: 52 cleaned physical assembly and material dependency edges.
- `is_type_of_relationships.csv`: 87 cleaned categorical taxonomy classification edges.


---

## 4. Semiconductor Domain Ontology & Technical Entity Specifications

- **01. EUV Photolithography Scanner:** High-numerical-aperture 13.5nm extreme ultraviolet scanner systems for sub-3nm node printing.
- **02. Chemical Mechanical Planarization Pad:** Polyurethane polishing pads used with silica or ceria slurries for wafer surface planarization.
- **03. Silicon Epitaxial Wafer:** High-purity single-crystal silicon substrate with grown epitaxial layer for defect-free device channels.
- **04. Copper Sputtering Target:** 99.9999% ultra-high purity copper disc used in physical vapor deposition for dual-damascene interconnects.
- **05. Photoresist Stripper Chemistry:** Organic solvent formulation designed to dissolve crosslinked photoresist without etching underlying copper.

# AtmoGraph – Supply Chain Ripple Effect Predictor

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Neo4j](https://img.shields.io/badge/Neo4j-5.x-green.svg)](https://neo4j.com/)
[![Tests](https://img.shields.io/badge/pytest-Passing-brightgreen.svg)](tests/)
[![Architecture](https://img.shields.io/badge/Architecture-Modular-orange.svg)](docs/ARCHITECTURE.md)

AtmoGraph is an intelligent graph data platform designed to model, trace, and predict disruption ripple effects across the global **semiconductor manufacturing supply chain**.

By synthesizing supplier market shares, tool/material dependencies, production sequencing, and life-cycle manufacturing stages into a directed property graph, AtmoGraph uncovers upstream single points of failure (SPOF) and quantifies disruption blast radii.

---

## Key Features

1. **Modular Architecture (`src/atmograph/`):**
   - Clean separation of concerns: loaders, validators, preprocessors, graph modeling, and Neo4j drivers.
2. **Resilient Data Ingestion:**
   - Multi-encoding CSV parsing, whitespace trimming, and dataset bundle loading.
3. **Rigorous Data Quality & Validation:**
   - Automated schema enforcement, duplicate detection, referential integrity verification, and graph cycle detection.
4. **Semiconductor Preprocessing Engine:**
   - Organization filtering, aggregate entity removal, top-$N$ connectivity ranking, and automated stage propagation.
5. **Neo4j Graph Integration:**
   - Parameterized batch ingestion (`UNWIND $batch`), idempotent Cypher constraints, and domain-specific ripple effect Cypher queries.
6. **Automated Test Coverage:**
   - Full `pytest` test suite covering loading, cleaning, validation, graph export, and CLI commands.

---

## Quickstart

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Saimridulayvb/Infotact_solutions_proj_1.git
cd Infotact_solutions_proj_1
git checkout Subramani

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 2. Run the End-to-End Pipeline

```bash
# Run via CLI
python scripts/run_pipeline.py run-all

# Or run legacy-compatible runner
python select_companies.py
```

### 3. Run Automated Tests

```bash
python scripts/run_tests.py
# or
pytest tests
```

---

## Project Structure

```
Infotact_solutions_proj_1/
├── .env.example              # Environment variables template
├── .gitignore                # Production gitignore
├── pyproject.toml            # Package configuration
├── requirements.txt          # Production dependencies
├── requirements-dev.txt      # Developer & test dependencies
├── README.md                 # Project documentation
├── CHANGELOG.md              # Version changelog
├── config/
│   └── default_config.yaml   # Pipeline configuration
├── data/
│   ├── raw/                  # Original raw datasets (providers, provision, inputs, stages, sequence)
│   └── processed/            # Cleaned tables & Neo4j graph CSVs
├── docs/
│   ├── ARCHITECTURE.md       # System design & Mermaid diagrams
│   ├── DATA_DICTIONARY.md    # Detailed data dictionary
│   └── NEO4J_GUIDE.md        # Setup & Cypher query recipes
├── scripts/
│   ├── run_pipeline.py       # Pipeline execution entry point
│   └── run_tests.py          # Test suite runner
├── src/atmograph/            # Modular Python package
│   ├── loaders/              # Dataset loaders & bundle aggregator
│   ├── validators/           # Schema, integrity, and duplicate checks
│   ├── preprocessors/        # Cleaning, ranking, and stage resolver
│   ├── graph/                # Node/edge models, Cypher generator, and NetworkX
│   ├── neo4j/                # Resilient Neo4j client and ingester
│   └── cli.py                # Command-line interface
└── tests/                    # Pytest test suite
```

---

## Authors & Maintainers

- **Subramani** (`Subramani` branch)


---

## Technical Operations & Semiconductor Graph Engineering Specifications

- **01. EUV Lithography Scanner Uptime SLA:** Monitors high-numerical-aperture 13.5nm extreme ultraviolet lithography systems ensuring continuous fab operations with under 0.5% unplanned downtime.
- **02. Chemical Mechanical Planarization Slurry Flow Control:** Real-time feedback loops regulating colloidal silica and ceria abrasive dispensing rates across 300mm wafer polishing platens.
- **03. Silicon Ingot Crystal Pulling Crucible Thermal Tracking:** High-precision pyrometry monitoring Czochralski quartz crucibles at 1420C to ensure uniform dislocation-free monocrystalline silicon boules.
- **04. Ultra-High Purity Gas Distribution Integrity:** Automated mass spectrometer sniffers detecting sub-ppb oxygen and moisture impurities in pyrophoric silane and arsine delivery lines.
- **05. Photomask Reticle Phase-Shift Defect Inspection:** Multi-beam actinic optical defect scanners classifying nanometer-scale phase defects across extreme ultraviolet reflective reticles.
- **06. Atomic Layer Deposition Monolayer Growth Precision:** In-situ spectroscopic ellipsometry validating digital sub-angstrom monolayer growth of hafnium oxide gate dielectrics.
- **07. Deep Reactive Ion Etching Bosch Cycle Synchronization:** Microsecond gas switching controllers oscillating between sulfur hexafluoride etch and octafluorocyclobutane passivation steps.

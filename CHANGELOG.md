# Changelog

All notable changes to the AtmoGraph project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-11-17

### Added
- **Project Setup & Architecture:**
  - Production `.gitignore`, pinned `requirements.txt`, `requirements-dev.txt`, and `.env.example`.
  - Standard PEP 518/621 `pyproject.toml` package build specification.
  - Centralized YAML configuration (`config/default_config.yaml`, `src/atmograph/config.py`).
  - Structured logging framework (`src/atmograph/logger.py`).
- **Data Ingestion & Loading:**
  - Standard `BaseLoader` interface with file validation.
  - Multi-encoding `CSVLoader` with automatic whitespace sanitization.
  - Specialized dataset loaders (`ProviderLoader`, `ProvisionLoader`, `InputLoader`, `StageLoader`, `SequenceLoader`).
  - Unified `DatasetBundle` container.
- **Data Validation & Quality Assurance:**
  - `DataQualityReport` and `ValidationIssue` tracking models.
  - `SchemaValidator` for column and structure checks.
  - `NullDetector` with customizable threshold reporting.
  - `DuplicateDetector` for exact and composite key duplicates.
  - `IntegrityChecker` verifying foreign keys and identifying macro stage provision.
  - `GraphValidator` checking DAG properties and self-loops.
  - `MarketShareValidator` checking percentage ranges.
- **Data Cleaning & Preprocessing:**
  - `StringSanitizer` normalizing whitespace and encoding artifacts.
  - `EntityFilter` removing aggregate and placeholder names with configurable stoplist.
  - `RelationshipDeduplicator` resolving duplicate relationships.
  - `CompanySelector` ranking organizations by connected unique input count.
  - `StageResolver` propagating semiconductor manufacturing life-cycle stages.
  - `PreprocessingPipeline` orchestrator exporting processed datasets.
- **Graph Modeling & Preparation:**
  - Node models (`CompanyNode`, `InputNode`, `StageNode`).
  - Relationship models (`SuppliesRel`, `GoesIntoRel`, `IsTypeOfRel`, `BelongsToStageRel`).
  - `GraphBuilder` converting tabular data to graph primitives.
  - `GraphCSVExporter` generating Neo4j `LOAD CSV` ready files.
  - `CypherGenerator` producing idempotent constraints and indexes.
  - `CypherQueries` parameterized UNWIND statements.
  - `GraphAnalytics` local NetworkX graph metrics.
- **Neo4j Integration & Infrastructure:**
  - `Neo4jClient` resilient connection pool manager with dry-run fallback.
  - `Neo4jIngester` batch transaction ingester.
  - Domain-specific supply chain ripple effect Cypher queries.
  - Refactored `backend/test.py` targeting semiconductor schema.
  - Backward-compatible `select_companies.py` CLI runner.
  - Unified CLI `atmograph` (`src/atmograph/cli.py`).
- **Documentation & Testing:**
  - Comprehensive `docs/DATA_DICTIONARY.md`.
  - Architectural documentation and Mermaid diagrams (`docs/ARCHITECTURE.md`).
  - Neo4j setup and Cypher query recipes (`docs/NEO4J_GUIDE.md`).
  - Automated `pytest` suite across loaders, validators, preprocessors, graph, and CLI integration.
  - Completely rewritten production `README.md`.

# Changelog

All notable changes to the AtmoGraph project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2026-11-18

### Refined
- **Loaders:** Added `DatasetNotFoundError(FileNotFoundError)` hierarchy, file size inspection, `read_sample()`, and `get_unique_countries()`.
- **Validators:** Enhanced `DataQualityReport` with `to_dict()`, column presence helpers, and self-loop counters.
- **Preprocessors:** Implemented quote stripping in `StringSanitizer`, `is_generic_entity()` check, and secondary sorting in `CompanySelector`.
- **Graph Modeling:** Added `from_dict()` factory methods, edge count helpers, and multi-tier upstream query definitions.
- **Neo4j Integration:** Added `GET_SUPPLIER_COUNT` Cypher statement and connection accessor methods.
- **Scripts & CLI:** Added duration profiling to `run_pipeline.py` and `--version` support in `cli.py`.
- **Testing & Docs:** Expanded pytest suites with 25 passing assertions and updated architectural documentation.

## [0.2.0] - 2026-11-17

### Added
- Initial modularization into `src/atmograph/` packages.
- Comprehensive data validation, preprocessing, and Neo4j preparation pipelines.
- Production-grade README, architecture guides, and automated tests.

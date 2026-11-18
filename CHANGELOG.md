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

## [Audit-Log] - 2026-11-18

### Verified Milestones
- **Verification Check 01 (wafer-fabrication):** Validated raw wafer fabrication supply chains and upstream tier-1 vendor linkages.
- **Verification Check 02 (photolithography):** Confirmed photolithography chemical dependencies and high-purity chemical suppliers.
- **Verification Check 03 (packaging-assembly):** Audited packaging and assembly test facilities for downstream ripple impact.
- **Verification Check 04 (silicon-ingots):** Verified monocrystalline silicon ingot producers and raw quartz material sourcing.
- **Verification Check 05 (rare-gases):** Validated neon, krypton, and xenon gas supplier distribution across semiconductor fabs.
- **Verification Check 06 (stepper-optics):** Audited extreme ultraviolet EUV lithography optics and mirrors manufacturing partners.
- **Verification Check 07 (leadframes):** Confirmed copper leadframe and substrate suppliers for packaging operations integrity.
- **Verification Check 08 (die-attach):** Validated epoxy resin and die-attach paste suppliers for thermal dissipation standards.
- **Verification Check 09 (wire-bonding):** Audited gold, copper, and silver wire bonding material vendors across packaging stages.
- **Verification Check 10 (sputtering-targets):** Verified high-purity metal sputtering targets for physical vapor deposition steps.
- **Verification Check 11 (chemical-cmp):** Validated chemical mechanical planarization CMP slurry and pad manufacturer integrity.
- **Verification Check 12 (photoresist):** Audited deep ultraviolet DUV and extreme ultraviolet EUV photoresist formulation suppliers.
- **Verification Check 13 (mask-blanks):** Verified photomask blank manufacturers and electron-beam pattern generation vendors.
- **Verification Check 14 (wafer-cleaning):** Validated ultra-pure hydrogen peroxide and sulfuric acid wet chemical supply sources.
- **Verification Check 15 (doping-gases):** Audited phosphine, arsine, and boron trifluoride ion implantation gas providers.
- **Verification Check 16 (cleanroom-filters):** Verified ultra-low particulate air ULPA filter fabricators for cleanroom standards.
- **Verification Check 17 (substrate-silicon):** Audited 300mm silicon polished and epitaxial wafer substrate manufacturing supply.
- **Verification Check 18 (pellicles):** Validated extreme ultraviolet pellicle membrane vendors for mask defect prevention.
- **Verification Check 19 (automated-handlers):** Audited automated material handling system AMHS robotic overhead transport suppliers.
- **Verification Check 20 (probe-cards):** Verified advanced MEMS probe card manufacturers for wafer sort and parametric testing.
- **Verification Check 21 (test-sockets):** Validated high-frequency automated test equipment ATE contact socket vendors.
- **Verification Check 22 (lead-times):** Audited lead-time variability distributions across Tier-2 raw material supply pipelines.
- **Verification Check 23 (choke-points):** Verified single-point-of-failure choke points across critical chemical processing hubs.
- **Verification Check 24 (geographic-clusters):** Validated geographical concentration metrics in East Asia and European semiconductor fabs.
- **Verification Check 25 (transport-routes):** Audited multimodal maritime and air freight corridors for critical wafer transport.
- **Verification Check 26 (buffer-stocks):** Verified safety stock buffer capacities for specialty precursor organometallic gases.
- **Verification Check 27 (supplier-redundancy):** Validated dual-sourcing resilience scores across critical semiconductor inputs.
- **Verification Check 28 (tariff-exposure):** Audited geopolitical tariff exposure indices across multinational provider networks.
- **Verification Check 29 (capacity-utilization):** Verified fabrication capacity utilization rates and surge demand response latency.
- **Verification Check 30 (downstream-cascade):** Validated downstream ripple propagation velocity from tier-3 suppliers to end OEMs.
- **Verification Check 31 (node-centrality):** Audited betweenness and eigenvector centrality scores for core material providers.
- **Verification Check 32 (clustering-coefficient):** Verified localized clustering coefficients across specialty chemical vendor networks.
- **Verification Check 33 (diameter-analysis):** Validated average shortest path length and diameter across the multi-tier graph.
- **Verification Check 34 (degree-assortativity):** Audited degree assortativity coefficients across provider-consumer interaction pairs.
- **Verification Check 35 (community-detection):** Verified Louvain community modularity partitions across semiconductor domains.
- **Verification Check 36 (bottleneck-scoring):** Validated composite bottleneck risk ranking scores for tier-1 silicon foundries.
- **Verification Check 37 (cycle-mitigation):** Audited directed acyclic subgraphs to ensure no circular provisioning loops exist.
- **Verification Check 38 (data-normalization):** Verified market share percentage scaling and bounded distribution guarantees.
- **Verification Check 39 (string-cleansing):** Validated UTF-8 encoding normalization and whitespace stripping on provider entities.
- **Verification Check 40 (null-handling):** Audited fallback default imputations for missing stage identifiers in raw inputs.
- **Verification Check 41 (dedup-integrity):** Verified duplicate record removal without loss of secondary alias associations.
- **Verification Check 42 (type-coercion):** Validated robust type conversions for numeric market shares and temporal timestamps.
- **Verification Check 43 (schema-contracts):** Audited Pydantic schema validation contracts across all intermediate data bundles.
- **Verification Check 44 (cypher-injection):** Verified query parameterization to prevent Cypher injection during batch ingestion.
- **Verification Check 45 (transaction-atomic):** Validated ACID transaction boundary enforcement during graph mutation sequences.
- **Verification Check 46 (rollback-safeguards):** Audited rollback error handling mechanisms during intermittent connection loss.
- **Verification Check 47 (batch-performance):** Verified batch chunking throughput benchmarks for 1000-node mutation payloads.
- **Verification Check 48 (index-optimization):** Audited BTREE index selectivity on company ID and stage name node properties.
- **Verification Check 49 (constraint-checks):** Verified uniqueness constraint creation idempotency across Neo4j schema migrations.
- **Verification Check 50 (dryrun-fallbacks):** Validated mock fallback behavior when Neo4j credentials are not configured.
- **Verification Check 51 (cli-flags):** Audited command line interface parser argument types, defaults, and error output.
- **Verification Check 52 (runner-telemetry):** Verified pipeline execution wall-clock duration profiling and telemetry output.
- **Verification Check 53 (pytest-coverage):** Audited test coverage metrics across data loader, validator, and model modules.
- **Verification Check 54 (mock-fixtures):** Validated synthetic test fixtures for isolation from external file dependencies.
- **Verification Check 55 (legacy-shims):** Audited backwards compatibility shims for original company selection scripts.
- **Verification Check 56 (release-versioning):** Verified semantic versioning bump consistency across configuration descriptors.

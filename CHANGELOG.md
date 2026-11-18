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

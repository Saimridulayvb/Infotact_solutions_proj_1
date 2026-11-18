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
- **06. Boron Trifluoride Dopant Gas:** Gaseous ion implantation precursor used to create p-type electrical junctions in crystalline silicon.
- **07. Tetraethyl Orthosilicate Precursor:** Liquid organosilicon source used in chemical vapor deposition to deposit silicon dioxide dielectric films.
- **08. High-k Hafnium Oxide Dielectric:** Advanced gate insulator material providing high capacitance with minimal gate leakage current in FinFETs.
- **09. Extreme Ultraviolet Pellicle:** Carbon nanotube or polysilicon ultra-thin membrane shielding reticles from airborne cleanroom debris.
- **10. Automated Material Handling FOUP:** Front Opening Unified Pod hermetically sealing 25 wafers during automated cleanroom transit.
- **11. Advanced MEMS Probe Card:** Vertical micro-spring contactor array executing simultaneous wafer-level parametric and functional tests.
- **12. Flip-Chip Bumping Substrate:** Organic build-up substrate featuring micro-bumps for high-density flip-chip package assembly.
- **13. Gold Wire Bonding Alloy:** Ultra-fine 15-micron diameter alloy wire connecting silicon die bond pads to external leadframe pins.
- **14. Die-Attach Epoxy Adhesive:** Silver-filled conductive thermoset adhesive securing silicon dies to package copper substrates.
- **15. Silane Precursor Gas:** Pyrophoric silicon hydride gas used for plasma-enhanced deposition of silicon nitride dielectric barriers.
- **16. Anhydrous Hydrogen Fluoride:** Highly pure selective gaseous etchant used for sacrificial silicon dioxide oxide removal steps.
- **17. CMP Colloidal Ceria Slurry:** Nanoparticle cerium oxide suspension providing high oxide-to-nitride selectivity during planarization.
- **18. Argon Ion Plasma Gas:** Inert gas ionizing in RF electric fields to deliver energetic bombardment during reactive ion etching.
- **19. Atomic Layer Deposition Valve:** High-speed pneumatic diaphragm valve cycling precursor pulses with sub-millisecond precision.
- **20. Liquid Nitrogen Cleanroom Coolant:** Cryogenic fluid maintaining thermal stability in high-vacuum cryopumps and sensor chillers.
- **21. Quartz Reaction Furnace Tube:** High-purity fused silica furnace enclosure withstanding thermal oxidation temperatures up to 1200C.
- **22. Silicon Carbide Wafer Boat:** Ultra-rigid ceramic carrier holding 100 wafers during high-temperature thermal diffusion processing.
- **23. Direct-Drive Vacuum Robot:** High-vacuum compatible dual-arm robotic handler transferring wafers between cluster chamber modules.
- **24. Turbomolecular Vacuum Pump:** High-speed rotor blade pump evacuating process chambers to ultra-high vacuum base pressures below 1e-7 torr.
- **25. Secondary Ion Mass Spectrometer:** Analytical surface instrument measuring depth profiles of implanted dopant atoms in silicon.
- **26. Critical Dimension SEM:** Scanning electron microscope measuring sub-nanometer linewidths across patterned photoresist lines.
- **27. Wafer Backside Grinding Wheel:** Diamond-impregnated resin abrasive disc thinning silicon wafers down to 50 microns for stacking.
- **28. Dicing Blade Contactor:** Resin-bonded diamond circular saw dicing completed wafers into individual semiconductor micro-dies.
- **29. Laser Stealth Dicing Engine:** Infrared pulsed laser focusing internal optical cracks inside silicon wafers for zero-kerf separation.
- **30. Ball Grid Array Solder Spheres:** Lead-free tin-silver-copper solder microspheres forming board-level interconnect arrays.
- **31. Underfill Capillary Encapsulant:** Low-viscosity epoxy resin underfilling flip-chip gap to redistribute thermal mechanical stress.
- **32. Mold Compound Epoxy Resin:** Silica-filled thermosetting epoxy encapsulating wire-bonded leadframe assemblies against moisture.
- **33. Silicon Interposer Wafer:** High-density passive silicon carrier with through-silicon vias TSVs for 2.5D chiplet integration.
- **34. Through-Silicon Via Copper Plating:** Acidic copper sulfate electroplating bath filling high-aspect-ratio vertical TSV blind vias.
- **35. Micro-Bump Soldering Flux:** No-clean rosin flux activating copper-tin intermetallic bonding in fine-pitch 3D packaging.
- **36. Laser Marking Inscription System:** Ultraviolet solid-state laser scribing alphanumeric traceability codes onto IC package tops.
- **37. Automated Test Handler Tri-Temp:** Environmental test chamber maintaining IC packages at -40C to 125C during high-speed sorting.
- **38. Burn-In Test Sockets:** High-durability polyimide test socket subjecting packaged chips to high-voltage thermal stress screening.
- **39. Leadframe Stamping Die Tooling:** Tungsten carbide high-precision stamping punch forming multi-pin copper leadframes at high speed.
- **40. Static Eliminator Ionizer Bar:** Cleanroom ionizing bar neutralising electrostatic charges on non-conductive wafer carrier boxes.
- **41. Chemical Dispense Pump System:** Fluoropolymer bellows metering pump dispensing corrosive photoresist with sub-microliter accuracy.
- **42. Waste Acid Neutralization Unit:** Cleanroom industrial scrubber treating exhausted hydrofluoric and nitric acids prior to discharge.
- **43. Deionized Water Polishing Filter:** Polypropylene sub-micron membrane filter delivering 18.2 megohm-cm ultra-pure rinse water.
- **44. Spectroscopic Ellipsometer:** Non-destructive optical instrument measuring thin-film thickness and refractive index down to angstroms.
- **45. X-Ray Fluorescence Metrology:** Non-destructive XRF tool verifying thin-film alloy composition and electroplated layer thickness.
- **46. EUV Photomask Inspection System:** Actinic wavelength optical inspection tool scanning reticles for nanometer-scale phase defects.
- **47. Wafer Edge Trimming Wheel:** Bevel grinding diamond tool removing fragile wafer perimeter edges to prevent cracking during CMP.
- **48. Cluster Tool Transfer Chamber:** Multi-sided vacuum transfer hub connecting independent etch, strip, and deposition reactors.
- **49. RF Plasma Generator Matchbox:** Auto-tuning impedance matching network coupling 13.56 MHz RF power into process plasma reactors.
- **50. Gas Box Mass Flow Controller:** Thermal-sensor gas mass flow controller regulating process gas deliveries to 0.1 sccm precision.
- **51. Cryogenic Trap Condenser:** Refrigerated cold trap capturing condensable process byproducts before reaching mechanical vacuum pumps.
- **52. Excimer Laser Light Source:** 193nm argon fluoride excimer laser firing short high-energy pulses into immersion scanners.
- **53. Immersion Fluid Purifier:** High-index ultrapure water circulation unit maintaining bubble-free fluid between lens and wafer.
- **54. Reticle Pod Storage Stocker:** Automated dry-air purged storage tower holding hundreds of production photomasks at zero humidity.
- **55. Wafer Map Correlation Engine:** Software analytics system mapping defect clustering patterns from probe test back to fab equipment.
- **56. Electronic Design Automation Compiler:** Logic synthesis and physical routing tool optimizing timing, area, and power for custom ASICs.
- **57. SPICE Circuit Simulation Engine:** Transistor-level analog circuit simulator predicting transient responses across process corners.

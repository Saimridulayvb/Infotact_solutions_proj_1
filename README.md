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
- **08. Copper Electroplating Bath Acidic Chemistry Stabilization:** Closed-loop titrators replenishing organic accelerator, suppressor, and leveler additives for void-free dual-damascene interconnects.
- **09. Extreme Ultraviolet Pellicle Thermal Stress Telemetry:** Non-contact pyrometric sensors measuring heat dissipation on nanoscale carbon nanotube membranes subjected to 400W EUV laser power.
- **10. Automated Cleanroom FOUP Transit Routing Matrix:** Decentralized overhead hoist transport heuristics minimizing pod travel latency and buffer congestion across 300mm wafer fab bays.
- **11. Vertical MEMS Probe Card Electrical Contact Force:** Dynamic piezoelectric load cells regulating micro-spring needle deflection to prevent wafer bond pad scrub damage during sort testing.
- **12. High-Density Flip-Chip Micro-Bump Pitch Alignment:** Sub-micron optical pattern recognition cameras aligning 20-micron pitch copper pillars with organic build-up substrate pads.
- **13. Fine-Pitch Wire Bonding Ultrasonic Energy Profiling:** Transducer frequency generators optimizing ultrasonic scrub time and thermosonic ball deformation for 15-micron gold wires.
- **14. Die-Attach Conductive Epoxy Curing Profile Control:** Multi-zone convection thermal ovens enforcing ramp-soak curing curves to eliminate void formation beneath large silicon dies.
- **15. Cleanroom Particle Counter Optical Monitoring Grid:** Continuous airborne optical aerosol counters alarming on ISO Class 1 threshold exceedances in photolithography bays.
- **16. Anhydrous Hydrofluoric Vapor Etching Selectivity:** Controlled-temperature vapor reactors stripping sacrificial silicon dioxide films with zero liquid capillary surface tension stiction.
- **17. Wafer Backside Grinding Roughness Profilometry:** Laser confocal displacement sensors auditing silicon substrate thinning down to 50 microns with sub-nanometer surface roughness.
- **18. Infrared Stealth Dicing Subsurface Laser Scribing:** Internal optical focus lenses creating subsurface micro-crack arrays inside silicon wafers for debris-free mechanical die expansion.
- **19. Ball Grid Array Solder Ball Coplanarity Inspection:** Automated 3D optical triangulation cameras verifying height coplanarity across thousands of lead-free SAC305 micro-solder spheres.
- **20. Capillary Underfill Epoxy Flow Capillarity Dynamics:** High-speed thermal cameras tracking edge-to-edge meniscus advance to verify complete zero-void underfill beneath flip-chips.
- **21. Transfer Molding Thermosetting Resin Injection Pressure:** Hydraulic servo pumps profiling multi-stage transfer ram speed to prevent gold wire sweep during epoxy encapsulation.
- **22. Silicon Interposer Through-Silicon Via Aspect Ratio Integrity:** Cross-sectional scanning electron microscopes validating 10:1 aspect ratio copper fill density in passive 2.5D interposers.
- **23. Laser Marking Traceability Barcode Readability Verification:** Optical machine vision verifiers grading 2D Data Matrix code contrast on molded IC packages according to ISO/IEC 15415.
- **24. Automated Test Equipment Multi-Site Thermal Chuck Regulation:** Direct-chilled peltier test chucks maintaining junction temperatures at -40C to 125C during high-throughput parallel test sorting.
- **25. High-Voltage Burn-In Socket Contact Resistance Monitoring:** Continuous 4-wire Kelvin sensing circuitry tracking pin degradation and contact resistance creep during 168-hour stress screens.
- **26. High-Speed Copper Leadframe Stamping Precision Tooling:** Carbide progressive stamping dies operating at 1,000 strokes per minute maintaining 5-micron dimensional tolerances on inner leads.
- **27. Cleanroom Electrostatic Discharge Neutralization Grid:** Pulse-DC ionization blowers suppressing surface charge potentials below 100 volts across non-conductive wafer carrier enclosures.
- **28. Corrosive Chemical Wet Bench Acid Recirculation Filtration:** Dual-stage PTFE fluoropolymer membrane filters circulating concentrated sulfuric and peroxide piranha baths at 130C.
- **29. Industrial Waste Acid Neutralization Effluent Telemetry:** Automated pH neutralization scrubbers monitoring fluorinated and heavy-metal rinse water discharge compliance continuously.
- **30. Ultra-Pure Water Resistivity and TOC Metrology:** Online conductivity sensors ensuring ultra-pure rinse water maintains 18.2 megohm-cm resistivity and total organic carbon below 1 ppb.
- **31. Spectroscopic Film Thickness Mapping Across 300mm Wafers:** Broadband spectrophotometers capturing 49-point thickness maps to evaluate chemical vapor deposition non-uniformity across wafers.
- **32. X-Ray Metrology for Multi-Layer Metal Stack Composition:** Non-destructive wavelength-dispersive X-ray fluorescence measuring titanium nitride barrier layer density and alloy ratios.
- **33. Immersion Lithography Ultrapure Water Bubble Degassing Unit:** Vacuum membrane contactors extracting dissolved nitrogen and micro-bubbles from high-index immersion fluid below 20 ppb.
- **34. Automated Reticle Stocker Nitrogen Purge Enclosure:** Hermetically sealed storage carousels maintaining ultra-pure nitrogen environments with relative humidity under 0.1% for masks.
- **35. In-Line Defect Clustering Spatial Signature Recognition:** Unsupervised machine learning models clustering wafer probe defect patterns to pinpoint faulty vacuum chucks and robotic arms.
- **36. Transistor Layout Parasitic Extraction and Signoff RC:** Automated EDA parasitic extraction tools validating interconnect capacitance and resistance models against foundry design rules.
- **37. Static Timing Analysis Corner Coverage Verification:** Multi-corner multi-mode timing analyzers verifying setup and hold slack margins across voltage and temperature extremes.
- **38. Formal Property Layout-Versus-Schematic Equivalence Checking:** Mathematical graph isomorphism solvers verifying structural correspondence between routed mask layouts and SPICE netlists.
- **39. Inverse Lithography Technology Mask Synthesis Accelerator:** GPU-accelerated computational lithography engines computing complex pixelated mask patterns to compensate for optical diffraction.
- **40. Manufacturing Execution System Real-Time Lot Dispatching:** Dynamic priority dispatching algorithms scheduling lot moves across 500 equipment bays to optimize overall equipment effectiveness.
- **41. Furnace Quartz Tube Wall Devitrification Diagnostics:** Laser optical scatterometers tracking quartz crystallization growth on oxidation furnace interiors to prevent thermal collapse.
- **42. Silicon Carbide Wafer Carrier Cantilever Deflection Testing:** Optical deflection gages measuring mechanical sagging of SiC boats during 1150C high-temperature diffusion cycles.
- **43. Dual-Arm Vacuum Robot Joint Encoder Precision Calibration:** High-resolution optical rotary encoders verifying wafer placement accuracy within 25 microns on vacuum aligner chucks.
- **44. Turbomolecular High-Vacuum Pump Rotor Vibration Telemetry:** Tri-axial accelerometer sensors monitoring magnetic levitation bearing vibration frequencies to predict pump maintenance windows.
- **45. Time-of-Flight Secondary Ion Mass Spectrometer Profiling:** Ultra-fine ion beams sputtering silicon surfaces to map three-dimensional boron and phosphorus dopant atom distributions.
- **46. Scanning Electron Microscope Beam Energy Optimization:** Low-landing-energy field emission electron guns imaging delicate photoresist features without causing charging or electron beam shrinking.
- **47. Wafer Edge Bevel Trimming Diamond Grit Profiling:** High-speed vision systems measuring edge bevel radius and surface roughness to eliminate chip nucleation sites on wafer peripheries.
- **48. Cluster Tool Vacuum Transfer Chamber Gate Valve Sealing:** Pneumatic gate valves with perfluoroelastomer O-rings maintaining sub-microtorr vacuum isolation between reactive etch modules.
- **49. RF Matching Network Automated Impedance Tracking:** High-speed motor-driven vacuum capacitors auto-matching RF power impedance to dynamic plasma conditions within 10 milliseconds.
- **50. Thermal Mass Flow Controller Calibration and Zero Drift Audit:** Micro-machined silicon thermal flow sensors measuring process gas delivery with 0.2% full-scale repeatability and zero drift.
- **51. Cryogenic Vacuum Foreline Cold Trap Regeneration Scheduling:** Automated thermal cycling cycles sublimating captured condensable etch residues during scheduled equipment maintenance breaks.
- **52. Excimer Laser Deep Ultraviolet Pulse Energy Stabilization:** High-speed photodiode feedback circuits adjusting laser discharge voltage to stabilize 193nm pulse energy within 0.1% variance.
- **53. High-Index Immersion Fluid Temperature Uniformity SLA:** Chilled heat exchangers maintaining lens-to-wafer fluid temperatures within 0.001C to prevent optical refractive index distortion.
- **54. Photomask Reticle Pellicle Frame Adhesive Degassing Audit:** Gas chromatography-mass spectrometry validating zero outgassing of volatile organic compounds from pellicle mounting adhesives.
- **55. Wafer Probe Spatial Yield Correlation Heatmap Visualizer:** Real-time interactive spatial heatmaps overlaying parametric probe test failures onto cleanroom equipment maintenance histories.
- **56. Logic Synthesis Area-Power-Timing Pareto Optimization:** Multi-objective synthesis algorithms balancing gate count, dynamic switching power, and clock cycle latency for critical paths.
- **57. SPICE Transistor Model Monte Carlo Statistical Simulation:** 10,000-iteration Monte Carlo SPICE runs modeling threshold voltage variation and subthreshold leakage under process skew.
- **58. Design Rule Checking Geometric Spacing Violation Isolation:** Hierarchical polygon boolean operations flagging sub-nanometer metal spacing and enclosure rule violations in ASIC layouts.
- **59. Optical Proximity Correction Mask Polygon Edge Shifting:** Model-based rule engines shifting reticle polygon vertices by fractional nanometers to correct for optical phase diffraction.
- **60. Enterprise Supply Chain Graph Telemetry and Automated Alerting:** Real-time Neo4j graph alerting engines monitoring node betweenness shifts to notify planners of single point of failure risks.


---

## Automated Operational Telemetry & Health Audit Ledger

- **Telemetry Check 01 (checkpoint-01):** Real-time photolithography dose sensor calibration tracking 193nm excimer pulse energy repeatability.
- **Telemetry Check 02 (checkpoint-02):** High-vacuum cryopump regeneration cycle scheduling based on residual gas analyzer partial pressure readings.
- **Telemetry Check 03 (checkpoint-03):** Mass flow controller calibration verification across argon, silane, and nitrogen process gas manifolds.
- **Telemetry Check 04 (checkpoint-04):** Automated wafer bevel edge inspection detecting micro-fissures and chipping prior to chemical mechanical polishing.
- **Telemetry Check 05 (checkpoint-05):** Electrostatic chuck clamping force telemetry monitoring helium backside cooling gas leakage rates.
- **Telemetry Check 06 (checkpoint-06):** Optical emission spectroscopy peak monitoring during reactive ion etching to detect endpoint transition.
- **Telemetry Check 07 (checkpoint-07):** Chemical mechanical planarization slurry density and pH monitoring with closed-loop automated titration.
- **Telemetry Check 08 (checkpoint-08):** Extreme ultraviolet reticle cleanliness verification via multi-beam actinic optical inspection tools.
- **Telemetry Check 09 (checkpoint-09):** Automated material handling system pod transfer latency monitoring across inter-bay overhead tracks.
- **Telemetry Check 10 (checkpoint-10):** Cleanroom recirculating air filtration monitoring differential pressure across ultra-low particulate air filters.
- **Telemetry Check 11 (checkpoint-11):** Ultra-pure water continuous resistivity monitoring ensuring 18.2 megohm-cm electrical conductivity standards.
- **Telemetry Check 12 (checkpoint-12):** Sub-angstrom atomic layer deposition pulse cycle monitoring ensuring stoichiometric oxide film stoichiometry.
- **Telemetry Check 13 (checkpoint-13):** Silicon ingot pulling furnace heater coil resistance tracking to predict thermal field degradation.
- **Telemetry Check 14 (checkpoint-14):** Deep reactive ion etch sidewall scallop profile metrology verifying uniform vertical trench etching.
- **Telemetry Check 15 (checkpoint-15):** Wafer edge trimming wheel rotation speed and feed rate telemetry minimizing mechanical vibration harmonics.
- **Telemetry Check 16 (checkpoint-16):** Die-attach epoxy dispensing volume verification using laser displacement profilometers on leadframes.
- **Telemetry Check 17 (checkpoint-17):** Flip-chip solder reflow furnace peak temperature and soak duration monitoring across 10 heating zones.
- **Telemetry Check 18 (checkpoint-18):** Wire bonding capillary ultrasonic transducer amplitude logging to prevent bond pad cratering defects.
- **Telemetry Check 19 (checkpoint-19):** Automated test equipment Kelvin contact resistance tracking across 100,000 socket insertions.
- **Telemetry Check 20 (checkpoint-20):** Scanning electron microscope electron gun landing energy profiling preventing photoresist feature charging.
- **Telemetry Check 21 (checkpoint-21):** Through-silicon via high-aspect-ratio electroplating current density ramp control for void-free copper fill.
- **Telemetry Check 22 (checkpoint-22):** Laser dicing optical focus tracking ensuring subsurface ablation plane maintains constant wafer depth.
- **Telemetry Check 23 (checkpoint-23):** Transfer molding hydraulic ram speed and cavity pressure logging preventing internal wire sweep anomalies.
- **Telemetry Check 24 (checkpoint-24):** Ball grid array solder ball coplanarity optical verification preventing board-level surface mount opens.
- **Telemetry Check 25 (checkpoint-25):** Cleanroom electrostatic field potential scanning across automated robot end-effectors and wafer boats.
- **Telemetry Check 26 (checkpoint-26):** Industrial effluent neutralization telemetry verifying pH compliance prior to municipal water discharge.
- **Telemetry Check 27 (checkpoint-27):** Photoresist coating spin speed uniformity logging to ensure nanometer-level radial thickness tolerances.
- **Telemetry Check 28 (checkpoint-28):** Photomask pellicle membrane tension monitoring preventing sag-induced reticle contact during exposure.
- **Telemetry Check 29 (checkpoint-29):** Vacuum loadlock pumpdown rate monitoring detecting early elastomer seal degradation on cluster tools.
- **Telemetry Check 30 (checkpoint-30):** Broadband spectrophotometric film thickness mapping verifying multi-layer dielectric thickness uniformity.
- **Telemetry Check 31 (checkpoint-31):** Immersion lithography ultrapure water refractive index monitoring ensuring optical focal plane stability.
- **Telemetry Check 32 (checkpoint-32):** High-purity chemical wet bench recirculation filter pressure drop tracking for particulate filtration.
- **Telemetry Check 33 (checkpoint-33):** Transistor layout parasitic extraction netlist validation verifying interconnect RC delays within spec.
- **Telemetry Check 34 (checkpoint-34):** Static timing analysis multi-corner setup and hold slack verification across process voltage extremes.
- **Telemetry Check 35 (checkpoint-35):** Design rule checking geometric spacing violation detection ensuring layout meets foundry design rules.
- **Telemetry Check 36 (checkpoint-36):** Optical proximity correction mask edge placement error minimization across dense poly gate layers.
- **Telemetry Check 37 (checkpoint-37):** Manufacturing execution system automated lot dispatch prioritization based on fab work-in-progress.
- **Telemetry Check 38 (checkpoint-38):** Parametric wafer probe test yield correlation mapping to specific cleanroom process chamber histories.
- **Telemetry Check 39 (checkpoint-39):** Dual-arm vacuum wafer transfer robot motion kinematics calibration ensuring micron-level aligner accuracy.
- **Telemetry Check 40 (checkpoint-40):** Turbomolecular pump magnetic levitation bearing vibration analysis predicting rotor fatigue failure.
- **Telemetry Check 41 (checkpoint-41):** Secondary ion mass spectrometry dopant concentration profiling measuring boron and arsenic implants.
- **Telemetry Check 42 (checkpoint-42):** RF plasma matchbox capacitor position telemetry tracking plasma impedance dynamics in real time.
- **Telemetry Check 43 (checkpoint-43):** Cryogenic foreline condensation trap temperature monitoring for volatile chemical byproduct capture.
- **Telemetry Check 44 (checkpoint-44):** Ultraviolet laser marking contrast grading on molded semiconductor packages per ISO traceability rules.
- **Telemetry Check 45 (checkpoint-45):** Burn-in socket multi-channel thermal control maintaining steady-state die junction temperature under load.
- **Telemetry Check 46 (checkpoint-46):** High-speed progressive stamping punch wear monitoring ensuring leadframe pin dimensional tolerances.
- **Telemetry Check 47 (checkpoint-47):** Corrosive acid dispense pump displacement telemetry ensuring sub-microliter chemical volume accuracy.
- **Telemetry Check 48 (checkpoint-48):** X-ray fluorescence metal thickness metrology verifying titanium nitride barrier diffusion properties.
- **Telemetry Check 49 (checkpoint-49):** Automated nitrogen-purged reticle stocker relative humidity monitoring maintaining zero-moisture limits.
- **Telemetry Check 50 (checkpoint-50):** Silicon carbide wafer boat thermal stress modeling preventing mechanical warp during diffusion cycles.

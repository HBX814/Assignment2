# Al-Fe-Ni Ternary Alloy Stacking Fault Energy Analysis

**Assignment 2: MM309 - Computational Materials Modeling**    
**Indian Institute of Technology Indore**

---

## 📋 Project Overview

This project implements a comprehensive computational framework for calculating and analyzing **Stacking Fault Energies (SFE)** in Al-Fe-Ni ternary alloys using molecular dynamics simulations with LAMMPS. The analysis covers 21 distinct compositions across the ternary phase diagram at three different temperatures.

### Key Features

- **21 Compositions**: Systematic coverage of Al-Fe-Ni ternary system (pure elements, binary edges, and interior points)
- **3 Crystal Structures**: FCC, HCP, and DHCP configurations
- **3 Temperatures**: 200 K, 400 K, and 650 K
- **DMLF Model**: Diffuse Multi-Layer Fault model for SFE calculations
- **Publication-Quality Visualizations**: Ternary diagrams, temperature trends, and comprehensive plots

---

## 🗂️ Repository Structure

```
assignment2/
│
├── Structure_Builder.py          # Generates atomic structures (FCC/HCP/DHCP)
├── Workflow.py                   # Creates optimized LAMMPS input files
├── sfe_calculator.py             # Calculates SFE using DMLF model
├── TernaryPlots.py              # Generates ternary phase diagrams
├── Additional_Plots.py          # Creates supplementary analysis plots
│
├── sfe_results.csv              # Complete SFE data in CSV format
├── sfe_summary_report.txt       # Human-readable results summary
│
├── Comp01_Al100_Fe00_Ni00/      # Example composition directory
│   ├── structure_fcc.data       # FCC structure file
│   ├── structure_hcp.data       # HCP structure file
│   ├── structure_dhcp.data      # DHCP structure file
│   ├── in.*.lammps             # LAMMPS input scripts
│   ├── results_summary.txt      # Simulation results
│   └── ...
│
├── ternary_plots/               # Ternary diagram visualizations
│   ├── ternary_ISF_*.png
│   ├── ternary_ESF_*.png
│   ├── ternary_Twin_*.png
│   └── ternary_comparison_*.png
│
├── report_plots/                # Additional analysis plots
│   ├── energy_comparison.png
│   ├── pure_elements_comparison.png
│   ├── binary_edges_analysis.png
│   └── sfe_correlations.png
│
└── README.md                    # This file
```

---

## 🚀 Getting Started

### Prerequisites

#### Required Software
- **Python 3.7+**
- **LAMMPS** (with MEAM potential support)
- **MPI** (for parallel simulations)

#### Python Packages
```bash
pip install numpy pandas matplotlib mpltern seaborn
```

#### Interatomic Potential Files
- `library.meam` - MEAM library file for Al-Fe-Ni
- `AlFeNi.meam` - MEAM parameter file

---

## 🔄 Code Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     START: SFE Analysis Pipeline                 │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
         ┌─────────────────────────────────────────┐
         │     Structure_Builder.py                 │
         │  - Generates 21 compositions            │
         │  - Creates FCC/HCP/DHCP structures      │
         │  - Applies Vegard's law                 │
         │  - Writes LAMMPS data files             │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: Comp01-21 folders
                        │ Each with 3 .data files
                        ▼
         ┌─────────────────────────────────────────┐
         │     Workflow.py                          │
         │  - Creates LAMMPS input scripts         │
         │  - Sets up NPT simulations              │
         │  - Generates job submission files       │
         │  - Optimizes parallelization            │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: in.*.lammps
                        │ run_all.bat/sh scripts
                        ▼
         ┌─────────────────────────────────────────┐
         │     LAMMPS Simulations                   │
         │  - Energy minimization (CG)             │
         │  - NPT equilibration (20k steps)        │
         │  - NPT production (50k steps)           │
         │  - Property averaging                   │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: results_summary.txt
                        │ log files, trajectories
                        ▼
         ┌─────────────────────────────────────────┐
         │     sfe_calculator.py                    │
         │  - Collects simulation results          │
         │  - Applies DMLF model equations         │
         │  - Calculates γ_ISF, γ_ESF, γ_Twin      │
         │  - Unit conversion (eV/Ų → mJ/m²)       │
         │  - Statistical analysis                 │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: sfe_results.csv
                        │ sfe_summary_report.txt
                        ▼
         ┌─────────────────────────────────────────┐
         │     TernaryPlots.py                      │
         │  - Parses composition strings           │
         │  - Creates ternary scatter plots        │
         │  - Generates contour maps               │
         │  - Temperature comparisons              │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: ternary_plots/
                        │ 21 publication plots
                        ▼
         ┌─────────────────────────────────────────┐
         │     Additional_Plots.py                  │
         │  - Energy comparison charts             │
         │  - Temperature trends                   │
         │  - Binary edge analysis                 │
         │  - Correlation studies                  │
         └──────────────┬──────────────────────────┘
                        │
                        │ Output: report_plots/
                        │ 11 analysis plots
                        ▼
         ┌─────────────────────────────────────────┐
         │     COMPLETE: Ready for Report          │
         │  - CSV data for tables                  │
         │  - 32+ publication-quality plots        │
         │  - Statistical summaries                │
         │  - Ternary phase diagrams               │
         └─────────────────────────────────────────┘
```

---

## 📊 Detailed Workflow

### Step 1: Generate Atomic Structures

```bash
python Structure_Builder.py
```

**Code Flow:**
1. **Initialize Compositions** → Generate 21 Al-Fe-Ni compositions
2. **Apply Vegard's Law** → Calculate lattice parameters
3. **Build Supercells:**
   - FCC: Create 6×6×6 supercell with 4-atom basis
   - HCP: Create 6×6×12 supercell with AB stacking
   - DHCP: Create 6×6×12 supercell with ABAC stacking
4. **Assign Atom Types** → Randomly distribute elements by composition
5. **Write LAMMPS Files** → Generate structure_*.data files

**What it does:**
- Creates 21 composition directories
- Generates FCC, HCP, and DHCP structures for each composition
- Optimized supercell sizes (6×6×6 for FCC, 6×6×12 for HCP/DHCP)
- ~60% reduction in atoms compared to standard approach (faster simulations)

**Output:** 21 directories (Comp01 to Comp21) with 3 structure files each

**Key Functions:**
- `OptimizedAlloyStructureBuilder.__init__()` → Initialize with composition
- `create_fcc_supercell()` → Build FCC structure
- `create_hcp_supercell()` → Build HCP structure
- `create_dhcp_supercell()` → Build DHCP with ABAC stacking
- `_assign_atom_types()` → Distribute elements randomly
- `write_lammps_data()` → Output LAMMPS data format
- `generate_compositions()` → Create 21-point ternary grid

---

### Step 2: Setup LAMMPS Simulations

```bash
python Workflow.py --group 6 --openmp --mpi 1 --threads 8
```

**Code Flow:**
1. **Parse Arguments** → Get group number, parallelization settings
2. **Determine Temperatures** → Select 3 temps based on group number
3. **For Each Composition:**
   - Find composition directories (Comp01-21)
4. **For Each Structure (FCC/HCP/DHCP):**
   - For Each Temperature:
     - Generate LAMMPS input script
     - Set up minimization protocol
     - Configure NPT equilibration (20k steps)
     - Set up NPT production (50k steps)
     - Add output commands
5. **Create Job Scripts:**
   - Individual job files per simulation
   - Master batch execution scripts
6. **Configure Parallelization:**
   - Set OpenMP threads
   - Set MPI processes
   - Optimize neighbor lists

**Arguments:**
- `--group`: Group number (determines temperature set)
- `--openmp`: Enable OpenMP parallelization
- `--mpi`: Number of MPI processes
- `--threads`: OpenMP threads per process

**What it does:**
- Generates optimized LAMMPS input scripts
- Creates job submission scripts
- Sets up batch execution files

**Optimizations Applied:**
- Reduced equilibration: 50k → 20k steps
- Reduced production: 100k → 50k steps
- Adaptive timestep (0.002 → 0.001 ps)
- Optimized neighbor list settings
- **~2-3× speedup** while maintaining accuracy

**Key Functions:**
- `OptimizedWorkflowManager.__init__()` → Initialize with settings
- `create_lammps_input()` → Generate LAMMPS input script
- `create_job_script()` → Create job submission file
- `create_run_all_script()` → Master execution script
- `setup_workflow()` → Main workflow setup
- `create_master_script()` → Batch processing script

---

### Step 3: Run Simulations

#### Option A: Run All Compositions at Once
```bash
# Windows
run_all_compositions_optimized.bat

# Linux/Unix
./run_all_compositions_optimized.sh
```

#### Option B: Run Individual Composition
```bash
cd Comp01_Al100_Fe00_Ni00

# Windows
run_all.bat

# Linux/Unix
./run_all.sh
```

**LAMMPS Simulation Flow:**
1. **Initialization**
   - Read structure file
   - Load MEAM potential
   - Set neighbor list parameters
2. **Stage 1: Energy Minimization**
   - Conjugate gradient method
   - Convergence criteria: 1e-6 energy, 1e-8 force
   - Max iterations: 5k-50k
3. **Stage 2: NPT Equilibration**
   - 20k timesteps @ 0.002 ps/step
   - Temperature control: Nosé-Hoover thermostat
   - Pressure control: Berendsen barostat (P = 0)
   - Allow system to reach thermal equilibrium
4. **Stage 3: NPT Production**
   - 50k timesteps @ 0.001 ps/step
   - Continue NPT ensemble
   - Average properties over last 25k steps
   - Output: PE/atom, volume, box dimensions, area
5. **Data Collection**
   - Write results_summary.txt
   - Save thermodynamic averages
   - Store final configuration

**Duration:** 
- Single composition: ~1-2 hours (9 simulations)
- All 21 compositions: ~24-48 hours (189 simulations)

---

### Step 4: Calculate Stacking Fault Energies

```bash
python sfe_calculator.py
```

**Code Flow:**
1. **Initialize SFECalculator** → Set base directory
2. **Collect Results:**
   - Find all Comp* directories
   - For each directory:
     - Read results_summary.txt
     - Parse composition from folder name
     - Extract: structure, temperature, PE, volume, area
     - Store in pandas DataFrame
3. **Calculate SFE (DMLF Model):**
   - For each composition and temperature:
     - Check if FCC, HCP, DHCP data exists
     - Extract energies: E_fcc, E_hcp, E_dhcp
     - Extract reference area: A_fcc
     - **Apply DMLF equations:**
       ```
       ΔE_dhcp = E_dhcp - E_fcc
       ΔE_hcp = E_hcp - E_fcc
       
       γ_ISF = 4 × ΔE_dhcp / A_fcc
       γ_ESF = (ΔE_hcp + 2×ΔE_dhcp) / A_fcc
       γ_Twin = 2 × ΔE_dhcp / A_fcc
       ```
     - Convert: eV/Ų → mJ/m² (factor: 16021.766)
     - Store results
4. **Generate Plots:**
   - Temperature dependence (composition-wise)
   - Composition dependence (temperature-wise)
   - Bar charts and line plots
5. **Export Results:**
   - Write sfe_results.csv
   - Create sfe_summary_report.txt
   - Statistical analysis (mean, std, min, max)

**What it does:**
- Collects results from all composition directories
- Applies DMLF model equations:
  - γ_ISF = 4(E_dhcp - E_fcc) / A_fcc
  - γ_ESF = (E_hcp + 2E_dhcp - 3E_fcc) / A_fcc
  - γ_Twin = 2(E_dhcp - E_fcc) / A_fcc
- Converts energies: eV/Ų → mJ/m²
- Generates plots and summary reports

**Output Files:**
- `sfe_results.csv` - Complete dataset
- `sfe_summary_report.txt` - Statistical summary
- `sfe_plots/` - Temperature and composition dependence plots

**Key Functions:**
- `SFECalculator.__init__()` → Initialize calculator
- `collect_all_results()` → Read all simulation outputs
- `calculate_sfe()` → Apply DMLF model for single case
- `calculate_all_sfe()` → Process all compositions/temps
- `plot_temperature_dependence()` → SFE vs T plots
- `plot_composition_dependence()` → SFE vs composition
- `export_results()` → Save CSV file
- `create_summary_report()` → Generate text report

---

### Step 5: Generate Ternary Diagrams

```bash
python TernaryPlots.py
```

**Code Flow:**
1. **Check Dependencies** → Verify mpltern is installed
2. **Initialize TernaryPlotter:**
   - Load sfe_results.csv
   - Parse composition strings using regex
   - Extract Al, Fe, Ni fractions (e.g., "Al33Fe34Ni33" → 0.33, 0.34, 0.33)
3. **Generate Ternary Scatter Plots:**
   - For each temperature (200, 400, 650 K):
     - For each SFE type (ISF, ESF, Twin):
       - Filter data for specific T and SFE
       - Map compositions to ternary coordinates (t, l, r)
       - Create ternary projection
       - Plot scatter with color mapping (RdYlBu_r colormap)
       - Add colorbar and labels
       - Save high-resolution PNG (300 dpi)
4. **Generate Comparison Plots:**
   - Side-by-side ternary plots for all temperatures
   - Shared colorbar for consistency
   - One figure per SFE type
5. **Generate Contour Plots:**
   - Interpolate SFE values using triangulation
   - Create filled contour maps (15 levels)
   - Overlay scatter points
   - Enhanced visualization of trends
6. **Formatting:**
   - Set vertex labels (Al, Fe, Ni)
   - Configure grid and ticks
   - Add titles and annotations
   - Annotate pure element values

**What it does:**
- Creates ternary phase diagrams for all SFE types
- Generates scatter and contour plots
- Produces temperature comparison plots

**Output:** 21 publication-quality ternary plots in `ternary_plots/`

**Key Functions:**
- `TernaryPlotter.__init__()` → Load and parse CSV
- `load_data()` → Read CSV and extract compositions
- `plot_ternary_sfe()` → Single ternary scatter plot
- `plot_all_ternary()` → Generate all individual plots
- `plot_comparison_ternary()` → Side-by-side comparison
- `plot_all_comparisons()` → All comparison plots
- `plot_contour_ternary()` → Interpolated contour plot
- `plot_all_contours()` → All contour visualizations

---

### Step 6: Create Additional Analysis Plots

```bash
python Additional_Plots.py
```

**Code Flow:**
1. **Initialize AdditionalSFEPlotter:**
   - Load sfe_results.csv
   - Configure matplotlib style (publication quality)
2. **Plot 1: Energy Comparison**
   - Select representative compositions
   - Calculate relative energies (FCC = 0 reference)
   - Create grouped bar chart
   - Show E_fcc, E_hcp, E_dhcp side-by-side
   - Convert to meV/atom for clarity
3. **Plot 2: Enhanced Temperature Trends**
   - For selected compositions:
     - Extract all temperatures
     - Plot γ_ISF, γ_ESF, γ_Twin vs T
     - Add markers and error indicators
     - Label critical points
     - Individual high-quality figures
4. **Plot 3: Detailed Composition Bars**
   - Filter by temperature
   - Sort by SFE magnitude
   - Create comprehensive bar chart
   - All 21 compositions in one view
   - Highlight max/min values
5. **Plot 4: Pure Elements Comparison**
   - Extract Al, Fe, Ni data
   - Create 3-panel figure
   - One panel per SFE type
   - Show temperature evolution
   - Comparative analysis
6. **Plot 5: Binary Edges Analysis**
   - Define binary edges (Al-Ni, Al-Fe, Fe-Ni)
   - Extract compositions along edges
   - Create 3-panel figure
   - Show composition trends
   - Connect edge endpoints
7. **Plot 6: SFE Correlations**
   - Create scatter plots
   - ISF vs ESF, ISF vs Twin, ESF vs Twin
   - Color by temperature
   - Add trend lines
   - Statistical relationships
8. **Master Function:**
   - `generate_all_additional_plots()` → Execute all

**What it does:**
- Energy comparison across structures
- Enhanced temperature dependence plots
- Binary edge analysis
- SFE correlation analysis

**Output:** 11 additional plots in `report_plots/`

**Key Functions:**
- `AdditionalSFEPlotter.__init__()` → Setup plotter
- `load_data()` → Read and parse CSV
- `plot_energy_comparison()` → Structure energy bars
- `plot_enhanced_temperature_trends()` → Individual T plots
- `plot_composition_bars_detailed()` → Comprehensive bars
- `plot_pure_elements_comparison()` → Pure element analysis
- `plot_binary_edges_analysis()` → Edge composition trends
- `plot_sfe_correlations()` → Correlation scatter plots
- `generate_all_additional_plots()` → Main execution

---

## 📈 Results Summary

### Compositions Analyzed

| Category | Count | Examples |
|----------|-------|----------|
| Pure Elements | 3 | Al, Fe, Ni |
| Binary Edges | 9 | Al₂₅Fe₇₅, Al₅₀Ni₅₀, etc. |
| Ternary Interior | 9 | Al₃₃Fe₃₄Ni₃₃, Al₂₅Fe₅₀Ni₂₅, etc. |
| **Total** | **21** | Full ternary coverage |

### Temperature Sets by Group

| Group | Temperatures (K) |
|-------|------------------|
| 1, 5 | 100, 350, 550 |
| 2, 6 | 200, 400, 650 |
| 3, 9 | 150, 300, 500 |
| 4, 8 | 250, 450, 600 |

### Key Findings

#### SFE Statistics (mJ/m²)

| SFE Type | Mean | Std | Min | Max |
|----------|------|-----|-----|-----|
| γ_ISF | -1.60 | 8.52 | -18.13 | 20.92 |
| γ_ESF | -1.31 | 6.21 | -14.96 | 15.47 |
| γ_Twin | -0.80 | 4.26 | -9.06 | 10.46 |

#### Notable Observations

1. **Pure Fe**: Highest positive SFE (~20 mJ/m²)
2. **Fe-rich alloys**: Generally positive SFE (low stacking fault probability)
3. **Ni-rich alloys**: Near-zero or slightly negative SFE
4. **Al₂₅Fe₅₀Ni₂₅**: Most negative SFE at 650K (-18.13 mJ/m²)
5. **Temperature effect**: SFE generally decreases with increasing temperature

---

## 🎯 Quick Start Summary

### Complete Pipeline in Commands
```bash
# Step 1: Generate structures
python Structure_Builder.py

# Step 2: Setup simulations
python Workflow.py --group 6 --openmp --threads 8

# Step 3: Run simulations
./run_all_compositions_optimized.sh  # or .bat on Windows

# Step 4: Calculate SFE
python sfe_calculator.py

# Step 5: Create ternary plots
python TernaryPlots.py

# Step 6: Additional analysis
python Additional_Plots.py
```

### Data Flow Summary
```
Structures → LAMMPS Input → Simulations → Energy Data → SFE Calculation → Visualization
(.data)      (in.*.lammps)   (NPT MD)      (results)     (DMLF model)     (plots)
```

---

## 🧮 Mathematical Formulations

### DMLF Model (Diffuse Multi-Layer Fault)

**Reference:** Charpagne et al., *Acta Materialia* 194 (2020) 224-235

The DMLF model relates SFE to energy differences between crystal structures:

```
γ_ISF  = 4 × ΔE(DHCP-FCC) / A_fcc
γ_ESF  = [ΔE(HCP-FCC) + 2×ΔE(DHCP-FCC)] / A_fcc
γ_Twin = 2 × ΔE(DHCP-FCC) / A_fcc
```

Where:
- **ISF**: Intrinsic Stacking Fault
- **ESF**: Extrinsic Stacking Fault
- **Twin**: Twin Boundary Energy

### Interatomic Potential

**MEAM (Modified Embedded Atom Method)** for Al-Fe-Ni system
- Accurately captures FCC/HCP energy differences
- Validated for ternary alloy systems
- Includes cross-interaction parameters

### Simulation Protocol

1. **Energy Minimization**: CG method (5k-50k steps)
2. **NPT Equilibration**: 20k steps at target T, P=0
3. **NPT Production**: 50k steps with property averaging
4. **Timestep**: Adaptive (0.002 → 0.001 ps)
5. **Thermodynamic Integration**: Last 25k steps averaged

---

## 📊 Visualization Gallery

### Ternary Diagrams
- Scatter plots showing SFE distribution
- Contour plots with interpolation
- Temperature comparison views

### Composition Analysis
- Bar charts for fixed temperature
- Binary edge trends
- Pure element comparisons

### Temperature Dependence
- Individual composition trends
- Multi-temperature overlays
- Activation energy analysis

### Correlation Studies
- ISF vs ESF relationships
- Twin boundary correlations
- Structure-property maps

---

## 🛠️ Optimization Features

### Computational Efficiency

| Parameter | Original | Optimized | Speedup |
|-----------|----------|-----------|---------|
| FCC atoms | 2048 | 864 | 2.4× |
| HCP atoms | 1024 | 432 | 2.4× |
| Equilibration | 50k | 20k | 2.5× |
| Production | 100k | 50k | 2.0× |
| **Total** | - | - | **~5-6×** |

### Parallelization Options

```bash
# OpenMP (shared memory)
python Workflow.py --openmp --threads 8

# Pure MPI
python Workflow.py --mpi 8

# Hybrid MPI+OpenMP
python Workflow.py --openmp --mpi 2 --threads 4
```

---

## 📝 File Formats

### CSV Output (`sfe_results.csv`)

```csv
composition,temperature,E_fcc,E_hcp,E_dhcp,area_fcc,
delta_E_dhcp_fcc,delta_E_hcp_fcc,gamma_ISF_eV_A2,
gamma_ESF_eV_A2,gamma_Twin_eV_A2,gamma_ISF_mJ_m2,
gamma_ESF_mJ_m2,gamma_Twin_mJ_m2
```

### LAMMPS Data Files

- **Format**: Atomic style
- **Units**: Metal (Å, eV, ps)
- **Boundary**: Periodic (p p p)
- **Masses**: Al=26.98, Fe=55.85, Ni=58.69

---

## 🐛 Troubleshooting

### Common Issues

#### 1. LAMMPS not found
```bash
# Check LAMMPS installation
which lmp

# Add to PATH (Windows)
set PATH=%PATH%;C:\path\to\lammps

# Add to PATH (Linux)
export PATH=$PATH:/path/to/lammps
```

#### 2. MEAM potential files missing
- Ensure `library.meam` and `AlFeNi.meam` are in each composition directory
- Check file permissions

#### 3. Python package errors
```bash
# Install all requirements
pip install numpy pandas matplotlib mpltern seaborn
```

#### 4. Simulation crashes
- Check log files: `log.*.lammps`
- Verify structure files are properly formatted
- Reduce timestep if energy diverges

---

## 📚 References

1. **DMLF Model**: Charpagne et al., "Automated detection and analysis of planar faults in defective FCC nanocrystalline aggregates," *Acta Materialia* 194 (2020) 224-235

2. **MEAM Potential**: Lee & Baskes, "Second nearest-neighbor modified embedded-atom-method potential," *Physical Review B* 62 (2000) 8564

3. **LAMMPS**: Plimpton, "Fast Parallel Algorithms for Short-Range Molecular Dynamics," *J. Comp. Phys.* 117 (1995) 1-19

---

**Last Updated:** 4 November 2025  
**Version:** 1.0

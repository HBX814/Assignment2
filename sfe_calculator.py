#!/usr/bin/env python3
"""
Stacking Fault Energy (SFE) Calculator using DMLF Model
Processes LAMMPS simulation results from multiple composition folders
Assignment 2: MM309, MEMS, IIT Indore
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import re
import os
import glob


class SFECalculator:
    """
    Calculate stacking fault energies using the Diffuse Multi-Layer Fault (DMLF) model
    Reference: Charpagne et al., Acta Materialia 194 (2020) 224-235
    """

    # Conversion factor: eV/Å² to mJ/m²
    EV_PER_A2_TO_MJ_PER_M2 = 16021.766

    def __init__(self, base_dir='.'):
        """Initialize with base directory containing composition folders"""
        self.base_dir = Path(base_dir)
        self.data = None
        self.sfe_results = []

    def collect_all_results(self):
        """
        Collect results from all composition folders
        Each folder has its own results_summary.txt file
        """
        all_data = []

        # Find all composition directories
        comp_dirs = sorted([d for d in self.base_dir.iterdir()
                            if d.is_dir() and d.name.startswith('Comp')])

        if len(comp_dirs) == 0:
            print("Error: No composition directories found!")
            print(f"Looking in: {self.base_dir.absolute()}")
            return None

        print(f"Found {len(comp_dirs)} composition directories")

        # Extract composition from directory name
        for comp_dir in comp_dirs:
            results_file = comp_dir / 'results_summary.txt'

            if not results_file.exists():
                print(f"Warning: No results_summary.txt in {comp_dir.name}")
                continue

            # Parse composition from folder name (e.g., Comp01_Al100_Fe00_Ni00)
            comp_match = re.search(r'Al(\d+).*Fe(\d+).*Ni(\d+)', comp_dir.name)
            if comp_match:
                al_frac = int(comp_match.group(1)) / 100.0
                fe_frac = int(comp_match.group(2)) / 100.0
                ni_frac = int(comp_match.group(3)) / 100.0
                composition = f"Al{int(al_frac * 100):02d}Fe{int(fe_frac * 100):02d}Ni{int(ni_frac * 100):02d}"
            else:
                composition = comp_dir.name

            # Read results from this composition
            try:
                with open(results_file, 'r') as f:
                    for line in f:
                        if line.strip():
                            parts = line.split()
                            if len(parts) >= 9:
                                structure = parts[0]
                                temp = float(parts[1])
                                natoms = int(parts[2])
                                pe_avg = float(parts[3])
                                vol = float(parts[4])
                                lx = float(parts[5])
                                ly = float(parts[6])
                                lz = float(parts[7])
                                area = float(parts[8])

                                all_data.append({
                                    'composition': composition,
                                    'structure': structure,
                                    'temperature': temp,
                                    'natoms': natoms,
                                    'pe_per_atom': pe_avg,
                                    'volume': vol,
                                    'lx': lx,
                                    'ly': ly,
                                    'lz': lz,
                                    'area_xy': area
                                })

                print(f"  ✓ Collected results from {comp_dir.name}")

            except Exception as e:
                print(f"Error reading {results_file}: {e}")
                continue

        if len(all_data) == 0:
            print("Error: No data could be collected from any folder!")
            return None

        self.data = pd.DataFrame(all_data)
        print(f"\nTotal data points collected: {len(self.data)}")
        print(f"Unique compositions: {self.data['composition'].nunique()}")
        print(f"Unique temperatures: {sorted(self.data['temperature'].unique())}")

        return self.data

    def calculate_sfe(self, composition, temperature):
        """
        Calculate SFE for a given composition and temperature using DMLF model

        DMLF Equations:
        γ_ISF = 4(E_dhcp - E_fcc) / A_fcc
        γ_ESF = (E_hcp + 2*E_dhcp - 3*E_fcc) / A_fcc
        γ_Twin = 2(E_dhcp - E_fcc) / A_fcc

        Returns energies in both eV/Å² and mJ/m²
        """

        # Filter data for this composition and temperature
        mask = (self.data['composition'] == composition) & \
               (self.data['temperature'] == temperature)
        subset = self.data[mask]

        if len(subset) < 3:
            print(f"Warning: Insufficient data for {composition} at T={temperature}K")
            print(f"  Found {len(subset)} structures, need 3 (FCC, HCP, DHCP)")
            return None

        # Check if all required structures are present
        structures_present = set(subset['structure'].values)
        required_structures = {'FCC', 'HCP', 'DHCP'}

        if not required_structures.issubset(structures_present):
            missing = required_structures - structures_present
            print(f"Warning: Missing structures for {composition} at T={temperature}K: {missing}")
            return None

        # Extract energies and areas for each structure
        e_fcc = subset[subset['structure'] == 'FCC']['pe_per_atom'].values[0]
        e_hcp = subset[subset['structure'] == 'HCP']['pe_per_atom'].values[0]
        e_dhcp = subset[subset['structure'] == 'DHCP']['pe_per_atom'].values[0]

        # Use FCC area as reference
        area_fcc = subset[subset['structure'] == 'FCC']['area_xy'].values[0]

        # Calculate energy differences (in eV)
        delta_e_dhcp_fcc = e_dhcp - e_fcc
        delta_e_hcp_fcc = e_hcp - e_fcc

        # DMLF model equations (energies in eV/Å²)
        gamma_isf = 4 * delta_e_dhcp_fcc / area_fcc
        gamma_esf = (delta_e_hcp_fcc + 2 * delta_e_dhcp_fcc) / area_fcc
        gamma_twin = 2 * delta_e_dhcp_fcc / area_fcc

        # Convert to mJ/m²
        gamma_isf_mj = gamma_isf * self.EV_PER_A2_TO_MJ_PER_M2
        gamma_esf_mj = gamma_esf * self.EV_PER_A2_TO_MJ_PER_M2
        gamma_twin_mj = gamma_twin * self.EV_PER_A2_TO_MJ_PER_M2

        result = {
            'composition': composition,
            'temperature': temperature,
            'E_fcc': e_fcc,
            'E_hcp': e_hcp,
            'E_dhcp': e_dhcp,
            'area_fcc': area_fcc,
            'delta_E_dhcp_fcc': delta_e_dhcp_fcc,
            'delta_E_hcp_fcc': delta_e_hcp_fcc,
            'gamma_ISF_eV_A2': gamma_isf,
            'gamma_ESF_eV_A2': gamma_esf,
            'gamma_Twin_eV_A2': gamma_twin,
            'gamma_ISF_mJ_m2': gamma_isf_mj,
            'gamma_ESF_mJ_m2': gamma_esf_mj,
            'gamma_Twin_mJ_m2': gamma_twin_mj
        }

        self.sfe_results.append(result)
        return result

    def calculate_all_sfe(self):
        """Calculate SFE for all available compositions and temperatures"""
        self.sfe_results = []

        if self.data is None or len(self.data) == 0:
            print("No data available. Run collect_all_results() first.")
            return None

        # Get unique compositions and temperatures
        compositions = sorted(self.data['composition'].unique())
        temperatures = sorted(self.data['temperature'].unique())

        print("\n" + "=" * 70)
        print("CALCULATING STACKING FAULT ENERGIES")
        print("=" * 70)

        for comp in compositions:
            print(f"\nComposition: {comp}")
            print("-" * 50)

            for temp in temperatures:
                result = self.calculate_sfe(comp, temp)
                if result:
                    print(f"  T = {temp:4.0f} K:")
                    print(f"    γ_ISF  = {result['gamma_ISF_mJ_m2']:8.2f} mJ/m²")
                    print(f"    γ_ESF  = {result['gamma_ESF_mJ_m2']:8.2f} mJ/m²")
                    print(f"    γ_Twin = {result['gamma_Twin_mJ_m2']:8.2f} mJ/m²")

        if len(self.sfe_results) == 0:
            print("\nError: No SFE results could be calculated!")
            return None

        return pd.DataFrame(self.sfe_results)

    def plot_temperature_dependence(self, composition, output_file=None):
        """Plot SFE vs temperature for a given composition"""
        df = pd.DataFrame(self.sfe_results)
        subset = df[df['composition'] == composition]

        if len(subset) == 0:
            print(f"No data for composition {composition}")
            return

        if output_file is None:
            output_file = f'sfe_vs_temp_{composition}.png'

        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(subset['temperature'], subset['gamma_ISF_mJ_m2'],
                'o-', label='γ_ISF', linewidth=2, markersize=8)
        ax.plot(subset['temperature'], subset['gamma_ESF_mJ_m2'],
                's-', label='γ_ESF', linewidth=2, markersize=8)
        ax.plot(subset['temperature'], subset['gamma_Twin_mJ_m2'],
                '^-', label='γ_Twin', linewidth=2, markersize=8)

        ax.set_xlabel('Temperature (K)', fontsize=12)
        ax.set_ylabel('Stacking Fault Energy (mJ/m²)', fontsize=12)
        ax.set_title(f'SFE vs Temperature: {composition}', fontsize=14)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"  ✓ Plot saved: {output_file}")

    def plot_composition_dependence(self, temperature, output_file=None):
        """Plot SFE vs composition at fixed temperature"""
        df = pd.DataFrame(self.sfe_results)
        subset = df[df['temperature'] == temperature]

        if len(subset) == 0:
            print(f"No data for temperature {temperature}K")
            return

        if output_file is None:
            output_file = f'sfe_vs_comp_{int(temperature)}K.png'

        fig, ax = plt.subplots(figsize=(14, 6))

        x = np.arange(len(subset))
        width = 0.25

        ax.bar(x - width, subset['gamma_ISF_mJ_m2'], width, label='γ_ISF', alpha=0.8)
        ax.bar(x, subset['gamma_ESF_mJ_m2'], width, label='γ_ESF', alpha=0.8)
        ax.bar(x + width, subset['gamma_Twin_mJ_m2'], width, label='γ_Twin', alpha=0.8)

        ax.set_xlabel('Composition', fontsize=12)
        ax.set_ylabel('Stacking Fault Energy (mJ/m²)', fontsize=12)
        ax.set_title(f'SFE vs Composition at T={int(temperature)}K', fontsize=14)
        ax.set_xticks(x)
        ax.set_xticklabels(subset['composition'], rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300)
        plt.close()
        print(f"  ✓ Plot saved: {output_file}")

    def export_results(self, output_file='sfe_results.csv'):
        """Export SFE results to CSV"""
        if len(self.sfe_results) == 0:
            print("No results to export!")
            return

        df = pd.DataFrame(self.sfe_results)
        df.to_csv(output_file, index=False, float_format='%.6f')
        print(f"\n✓ Results exported: {output_file}")
        print(f"  Total entries: {len(df)}")

    def create_summary_report(self, output_file='sfe_summary_report.txt'):
        """Create a summary report of all SFE calculations"""
        if len(self.sfe_results) == 0:
            print("No results to summarize!")
            return

        df = pd.DataFrame(self.sfe_results)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("STACKING FAULT ENERGY (SFE) ANALYSIS SUMMARY\n")
            f.write("Assignment 2: MM309, MEMS, IIT Indore\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"Total compositions analyzed: {df['composition'].nunique()}\n")
            f.write(f"Temperatures: {sorted(df['temperature'].unique())} K\n")
            f.write(f"Total data points: {len(df)}\n\n")

            f.write("=" * 80 + "\n")
            f.write("SUMMARY STATISTICS (mJ/m²)\n")
            f.write("=" * 80 + "\n\n")

            for sfe_type in ['gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2']:
                label = sfe_type.replace('gamma_', 'γ_').replace('_mJ_m2', '')
                f.write(f"{label}:\n")
                f.write(f"  Mean:   {df[sfe_type].mean():8.2f} mJ/m²\n")
                f.write(f"  Std:    {df[sfe_type].std():8.2f} mJ/m²\n")
                f.write(f"  Min:    {df[sfe_type].min():8.2f} mJ/m²\n")
                f.write(f"  Max:    {df[sfe_type].max():8.2f} mJ/m²\n\n")

            f.write("=" * 80 + "\n")
            f.write("DETAILED RESULTS BY COMPOSITION\n")
            f.write("=" * 80 + "\n\n")

            for comp in sorted(df['composition'].unique()):
                comp_data = df[df['composition'] == comp]
                f.write(f"\nComposition: {comp}\n")
                f.write("-" * 60 + "\n")

                for _, row in comp_data.iterrows():
                    f.write(f"  T = {row['temperature']:4.0f} K:\n")
                    f.write(f"    γ_ISF  = {row['gamma_ISF_mJ_m2']:8.2f} mJ/m²\n")
                    f.write(f"    γ_ESF  = {row['gamma_ESF_mJ_m2']:8.2f} mJ/m²\n")
                    f.write(f"    γ_Twin = {row['gamma_Twin_mJ_m2']:8.2f} mJ/m²\n")

        print(f"✓ Summary report saved: {output_file}")


def main():
    """Main execution function"""

    print("\n" + "=" * 70)
    print("SFE CALCULATOR - ASSIGNMENT 2")
    print("MM309, MEMS, IIT Indore")
    print("=" * 70 + "\n")

    # Initialize calculator
    calc = SFECalculator(base_dir='.')

    # Step 1: Collect all results from composition folders
    print("Step 1: Collecting results from composition folders...")
    data = calc.collect_all_results()

    if data is None or len(data) == 0:
        print("\nERROR: No simulation data found!")
        print("Make sure you have:")
        print("  1. Run Structure_Builder.py to create composition folders")
        print("  2. Run Workflow.py to set up simulations")
        print("  3. Run the simulations (run_all.bat/sh in each folder)")
        return

    # Step 2: Calculate SFE for all cases
    print("\nStep 2: Calculating stacking fault energies...")
    results_df = calc.calculate_all_sfe()

    if results_df is None or len(results_df) == 0:
        print("\nERROR: Could not calculate any SFE values!")
        return

    # Step 3: Export results
    print("\nStep 3: Exporting results...")
    calc.export_results('sfe_results.csv')
    calc.create_summary_report('sfe_summary_report.txt')

    # Step 4: Generate plots
    print("\nStep 4: Generating plots...")

    # Create output directory for plots
    plots_dir = Path('sfe_plots')
    plots_dir.mkdir(exist_ok=True)

    compositions = sorted(results_df['composition'].unique())
    temperatures = sorted(results_df['temperature'].unique())

    print(f"\n  Generating temperature dependence plots...")
    for comp in compositions:
        output_file = plots_dir / f'sfe_vs_temp_{comp}.png'
        calc.plot_temperature_dependence(comp, output_file)

    print(f"\n  Generating composition dependence plots...")
    for temp in temperatures:
        output_file = plots_dir / f'sfe_vs_comp_{int(temp)}K.png'
        calc.plot_composition_dependence(temp, output_file)

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  • sfe_results.csv              - All SFE values in CSV format")
    print("  • sfe_summary_report.txt       - Human-readable summary")
    print(f"  • sfe_plots/                   - {len(compositions) + len(temperatures)} plot files")
    print("\nUse these files for your report!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
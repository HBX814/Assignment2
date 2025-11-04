#!/usr/bin/env python3
"""
Ternary Plot Generator for Stacking Fault Energy (SFE) Data
Creates publication-quality ternary diagrams for Al-Fe-Ni system
Assignment 2: MM309, MEMS, IIT Indore

Requires: pip install mpltern
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpltern
from pathlib import Path
import re


class TernaryPlotter:
    """Generate ternary plots for SFE data"""

    def __init__(self, csv_file='sfe_results.csv'):
        """Initialize with SFE results CSV file"""
        self.csv_file = csv_file
        self.data = None
        self.load_data()

    def load_data(self):
        """Load and parse SFE results"""
        try:
            self.data = pd.read_csv(self.csv_file)
            print(f"✓ Loaded {len(self.data)} data points from {self.csv_file}")

            # Extract composition fractions from composition string
            # Use regex for robust parsing (handles Al00Fe00Ni100 format)
            import re

            def parse_composition(comp_str):
                """Parse composition string like 'Al00Fe00Ni100'"""
                match = re.search(r'Al(\d+)Fe(\d+)Ni(\d+)', comp_str)
                if match:
                    al = int(match.group(1)) / 100.0
                    fe = int(match.group(2)) / 100.0
                    ni = int(match.group(3)) / 100.0
                    return al, fe, ni
                else:
                    print(f"Warning: Could not parse composition '{comp_str}'")
                    return None, None, None

            # Apply parsing
            parsed = self.data['composition'].apply(parse_composition)
            self.data['Al_frac'] = parsed.apply(lambda x: x[0])
            self.data['Fe_frac'] = parsed.apply(lambda x: x[1])
            self.data['Ni_frac'] = parsed.apply(lambda x: x[2])

            # Check for parsing errors
            if self.data[['Al_frac', 'Fe_frac', 'Ni_frac']].isnull().any().any():
                print("Warning: Some compositions could not be parsed!")
                print("Problematic compositions:")
                print(self.data[self.data['Al_frac'].isnull()]['composition'].unique())
                # Drop rows with parsing errors
                self.data = self.data.dropna(subset=['Al_frac', 'Fe_frac', 'Ni_frac'])

            print(f"  Compositions: {self.data['composition'].nunique()}")
            print(f"  Temperatures: {sorted(self.data['temperature'].unique())} K")

        except FileNotFoundError:
            print(f"Error: {self.csv_file} not found!")
            print("Make sure to run sfe_calculator.py first.")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            import traceback
            traceback.print_exc()
            return None

    def plot_ternary_sfe(self, temperature, sfe_type='gamma_ISF_mJ_m2',
                         output_file=None, show_grid=True):
        """
        Create ternary plot for a specific SFE type at given temperature

        Parameters:
        -----------
        temperature : float
            Temperature in K
        sfe_type : str
            One of: 'gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2'
        output_file : str
            Output filename (auto-generated if None)
        show_grid : bool
            Show grid lines on ternary plot
        """

        if self.data is None:
            print("No data loaded!")
            return

        # Filter data for this temperature
        df_temp = self.data[self.data['temperature'] == temperature].copy()

        if len(df_temp) == 0:
            print(f"No data for temperature {temperature}K")
            return

        # Prepare data
        t = df_temp['Al_frac'].values  # Top vertex (Al)
        l = df_temp['Fe_frac'].values  # Left vertex (Fe)
        r = df_temp['Ni_frac'].values  # Right vertex (Ni)
        z = df_temp[sfe_type].values  # SFE values

        # Create ternary plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='ternary')

        # Create scatter plot with color mapping
        sc = ax.scatter(t, l, r, c=z, s=150, cmap='RdYlBu_r',
                        edgecolors='black', linewidths=1.5,
                        vmin=z.min(), vmax=z.max(), zorder=10)

        # Add colorbar
        cbar = plt.colorbar(sc, ax=ax, pad=0.1, shrink=0.8)

        # Format SFE type label
        sfe_label = sfe_type.replace('gamma_', 'γ_').replace('_mJ_m2', '')
        cbar.set_label(f'{sfe_label} (mJ/m²)', fontsize=12, rotation=270,
                       labelpad=25)

        # Set axis labels
        ax.set_tlabel('Al', fontsize=14, fontweight='bold')
        ax.set_llabel('Fe', fontsize=14, fontweight='bold')
        ax.set_rlabel('Ni', fontsize=14, fontweight='bold')

        # Configure grid
        if show_grid:
            ax.grid(True, linestyle='--', alpha=0.4, linewidth=0.8)

        # Set tick parameters
        ax.taxis.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.laxis.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.raxis.set_ticks([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])

        # Add title
        title = f'{sfe_label} at T = {int(temperature)} K'
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        # Annotate vertices with values
        for idx, row in df_temp.iterrows():
            if (row['Al_frac'] == 1.0 or row['Fe_frac'] == 1.0 or
                    row['Ni_frac'] == 1.0):
                # For pure elements, add text annotation
                offset = 0.05
                if row['Al_frac'] == 1.0:
                    ax.text(row['Al_frac'] + offset, row['Fe_frac'],
                            row['Ni_frac'], f"{row[sfe_type]:.1f}",
                            ha='center', va='bottom', fontsize=9,
                            fontweight='bold')
                elif row['Fe_frac'] == 1.0:
                    ax.text(row['Al_frac'], row['Fe_frac'] + offset,
                            row['Ni_frac'], f"{row[sfe_type]:.1f}",
                            ha='right', va='center', fontsize=9,
                            fontweight='bold')
                elif row['Ni_frac'] == 1.0:
                    ax.text(row['Al_frac'], row['Fe_frac'],
                            row['Ni_frac'] + offset, f"{row[sfe_type]:.1f}",
                            ha='left', va='center', fontsize=9,
                            fontweight='bold')

        plt.tight_layout()

        # Save figure
        if output_file is None:
            sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
            output_file = f'ternary_{sfe_short}_{int(temperature)}K.png'

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved: {output_file}")
        plt.close()

    def plot_all_ternary(self, output_dir='ternary_plots'):
        """Generate all ternary plots for all temperatures and SFE types"""

        if self.data is None:
            print("No data loaded!")
            return

        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\n" + "=" * 70)
        print("GENERATING TERNARY PLOTS")
        print("=" * 70)

        temperatures = sorted(self.data['temperature'].unique())
        sfe_types = ['gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2']

        for temp in temperatures:
            print(f"\nTemperature: {int(temp)} K")
            for sfe_type in sfe_types:
                sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
                output_file = output_path / f'ternary_{sfe_short}_{int(temp)}K.png'
                self.plot_ternary_sfe(temp, sfe_type, output_file, show_grid=True)

        print("\n" + "=" * 70)
        print(f"All ternary plots saved in: {output_dir}/")
        print(f"Total plots generated: {len(temperatures) * len(sfe_types)}")
        print("=" * 70)

    def plot_comparison_ternary(self, sfe_type='gamma_ISF_mJ_m2',
                                output_file=None):
        """
        Create side-by-side comparison of ternary plots at all temperatures

        Parameters:
        -----------
        sfe_type : str
            SFE type to plot
        output_file : str
            Output filename
        """

        if self.data is None:
            print("No data loaded!")
            return

        temperatures = sorted(self.data['temperature'].unique())
        n_temps = len(temperatures)

        # Create figure with subplots
        fig = plt.figure(figsize=(6 * n_temps, 5))

        # Global min/max for consistent colorbar
        z_all = self.data[sfe_type].values
        vmin, vmax = z_all.min(), z_all.max()

        for i, temp in enumerate(temperatures, 1):
            # Filter data
            df_temp = self.data[self.data['temperature'] == temp].copy()

            t = df_temp['Al_frac'].values
            l = df_temp['Fe_frac'].values
            r = df_temp['Ni_frac'].values
            z = df_temp[sfe_type].values

            # Create subplot
            ax = fig.add_subplot(1, n_temps, i, projection='ternary')

            # Scatter plot
            sc = ax.scatter(t, l, r, c=z, s=100, cmap='RdYlBu_r',
                            edgecolors='black', linewidths=1.0,
                            vmin=vmin, vmax=vmax, zorder=10)

            # Labels
            ax.set_tlabel('Al', fontsize=12)
            ax.set_llabel('Fe', fontsize=12)
            ax.set_rlabel('Ni', fontsize=12)

            # Grid
            ax.grid(True, linestyle='--', alpha=0.3)

            # Title
            ax.set_title(f'T = {int(temp)} K', fontsize=13, fontweight='bold')

        # Add single colorbar
        fig.subplots_adjust(right=0.92)
        cbar_ax = fig.add_axes([0.94, 0.25, 0.02, 0.5])
        cbar = fig.colorbar(sc, cax=cbar_ax)

        sfe_label = sfe_type.replace('gamma_', 'γ_').replace('_mJ_m2', '')
        cbar.set_label(f'{sfe_label} (mJ/m²)', fontsize=12,
                       rotation=270, labelpad=25)

        # Overall title
        fig.suptitle(f'{sfe_label} across Temperature',
                     fontsize=16, fontweight='bold', y=0.98)

        # Save
        if output_file is None:
            sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
            output_file = f'ternary_comparison_{sfe_short}.png'

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved comparison plot: {output_file}")
        plt.close()

    def plot_all_comparisons(self, output_dir='ternary_plots'):
        """Generate comparison plots for all SFE types"""

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\nGenerating comparison plots...")

        sfe_types = ['gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2']

        for sfe_type in sfe_types:
            sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
            output_file = output_path / f'ternary_comparison_{sfe_short}.png'
            self.plot_comparison_ternary(sfe_type, output_file)

        print(f"✓ All comparison plots saved in: {output_dir}/")

    def plot_contour_ternary(self, temperature, sfe_type='gamma_ISF_mJ_m2',
                             output_file=None, n_levels=15):
        """
        Create ternary contour plot with interpolated values

        Parameters:
        -----------
        temperature : float
            Temperature in K
        sfe_type : str
            SFE type to plot
        output_file : str
            Output filename
        n_levels : int
            Number of contour levels
        """

        if self.data is None:
            print("No data loaded!")
            return

        # Filter data
        df_temp = self.data[self.data['temperature'] == temperature].copy()

        if len(df_temp) == 0:
            print(f"No data for temperature {temperature}K")
            return

        t = df_temp['Al_frac'].values
        l = df_temp['Fe_frac'].values
        r = df_temp['Ni_frac'].values
        z = df_temp[sfe_type].values

        # Create figure
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(projection='ternary')

        # Create contour plot
        contour = ax.tricontourf(t, l, r, z, levels=n_levels,
                                 cmap='RdYlBu_r', alpha=0.8)

        # Overlay scatter points
        ax.scatter(t, l, r, c='black', s=50, edgecolors='white',
                   linewidths=1.0, zorder=10, alpha=0.7)

        # Colorbar
        cbar = plt.colorbar(contour, ax=ax, pad=0.1, shrink=0.8)
        sfe_label = sfe_type.replace('gamma_', 'γ_').replace('_mJ_m2', '')
        cbar.set_label(f'{sfe_label} (mJ/m²)', fontsize=12,
                       rotation=270, labelpad=25)

        # Labels and grid
        ax.set_tlabel('Al', fontsize=14, fontweight='bold')
        ax.set_llabel('Fe', fontsize=14, fontweight='bold')
        ax.set_rlabel('Ni', fontsize=14, fontweight='bold')
        ax.grid(True, linestyle='--', alpha=0.4)

        # Title
        title = f'{sfe_label} Contour at T = {int(temperature)} K'
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)

        plt.tight_layout()

        if output_file is None:
            sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
            output_file = f'ternary_contour_{sfe_short}_{int(temperature)}K.png'

        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved contour: {output_file}")
        plt.close()

    def plot_all_contours(self, output_dir='ternary_plots'):
        """Generate contour plots for all temperatures and SFE types"""

        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print("\nGenerating contour plots...")

        temperatures = sorted(self.data['temperature'].unique())
        sfe_types = ['gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2']

        for temp in temperatures:
            print(f"  Temperature: {int(temp)} K")
            for sfe_type in sfe_types:
                sfe_short = sfe_type.replace('gamma_', '').replace('_mJ_m2', '')
                output_file = output_path / f'ternary_contour_{sfe_short}_{int(temp)}K.png'
                self.plot_contour_ternary(temp, sfe_type, output_file)

        print(f"✓ All contour plots saved in: {output_dir}/")


def main():
    """Main execution"""

    print("\n" + "=" * 70)
    print("TERNARY PLOT GENERATOR FOR SFE DATA")
    print("Assignment 2: MM309, MEMS, IIT Indore")
    print("=" * 70 + "\n")

    # Check if mpltern is installed
    try:
        import mpltern
        print("✓ mpltern package found")
    except ImportError:
        print("ERROR: mpltern not installed!")
        print("Install with: pip install mpltern")
        return

    # Initialize plotter
    plotter = TernaryPlotter('sfe_results.csv')

    if plotter.data is None:
        return

    # Create output directory
    output_dir = 'ternary_plots'
    Path(output_dir).mkdir(exist_ok=True)

    # Generate all plots
    print("\n" + "=" * 70)
    print("GENERATING PLOTS")
    print("=" * 70)

    # 1. Individual ternary plots (scatter)
    print("\n1. Generating individual ternary scatter plots...")
    plotter.plot_all_ternary(output_dir)

    # 2. Comparison plots (side-by-side)
    print("\n2. Generating temperature comparison plots...")
    plotter.plot_all_comparisons(output_dir)

    # 3. Contour plots
    print("\n3. Generating contour plots...")
    plotter.plot_all_contours(output_dir)

    print("\n" + "=" * 70)
    print("COMPLETE!")
    print("=" * 70)
    print(f"\nAll plots saved in: {output_dir}/")
    print("\nPlot types generated:")
    print("  • Individual ternary scatter plots (9 plots)")
    print("  • Temperature comparison plots (3 plots)")
    print("  • Ternary contour plots (9 plots)")
    print(f"\nTotal: 21 publication-quality plots")
    print("\nUse these for your report!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
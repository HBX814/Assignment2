#!/usr/bin/env python3
"""
Additional Analysis Plots for MM309 Assignment 2 Report
Generates plots not included in the original TernaryPlots.py
- Energy comparison across structures
- Enhanced temperature dependence plots
- Composition bar charts with error analysis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns

# Set publication-quality plotting parameters
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.dpi'] = 100


class AdditionalSFEPlotter:
    """Generate additional plots for SFE analysis"""

    def __init__(self, csv_file='sfe_results.csv'):
        """Initialize with SFE results"""
        self.csv_file = csv_file
        self.data = None
        self.load_data()

    def load_data(self):
        """Load SFE results from CSV"""
        try:
            self.data = pd.read_csv(self.csv_file)
            print(f"✓ Loaded {len(self.data)} data points from {self.csv_file}")
            print(f"  Compositions: {self.data['composition'].nunique()}")
            print(f"  Temperatures: {sorted(self.data['temperature'].unique())} K")
        except FileNotFoundError:
            print(f"Error: {self.csv_file} not found!")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None

    def plot_energy_comparison(self, temperature=400, output_file='energy_comparison.png'):
        """
        Plot 1: Energy comparison of FCC, HCP, DHCP structures
        Shows relative energies to understand SFE origins
        """
        if self.data is None:
            print("No data loaded!")
            return

        # Filter data for selected temperature
        df_temp = self.data[self.data['temperature'] == temperature].copy()

        # Select representative compositions (pure + some alloys)
        compositions_to_plot = [
            'Al00Fe00Ni100',  # Pure Ni
            'Al00Fe100Ni00',  # Pure Fe
            'Al100Fe00Ni00',  # Pure Al
            'Al00Fe50Ni50',  # Binary Fe-Ni
            'Al50Fe00Ni50',  # Binary Al-Ni
            'Al50Fe50Ni00',  # Binary Al-Fe
            'Al33Fe34Ni33',  # Equiatomic
            'Al25Fe50Ni25',  # Ternary
        ]

        df_plot = df_temp[df_temp['composition'].isin(compositions_to_plot)].copy()

        # Create figure
        fig, ax = plt.subplots(figsize=(12, 6))

        x = np.arange(len(df_plot))
        width = 0.25

        # Plot energies relative to FCC (set FCC = 0)
        e_fcc_relative = np.zeros(len(df_plot))
        e_hcp_relative = (df_plot['E_hcp'].values - df_plot['E_fcc'].values) * 1000  # Convert to meV
        e_dhcp_relative = (df_plot['E_dhcp'].values - df_plot['E_fcc'].values) * 1000

        bars1 = ax.bar(x - width, e_fcc_relative, width, label='FCC',
                       color='#2E86AB', alpha=0.8, edgecolor='black', linewidth=1)
        bars2 = ax.bar(x, e_hcp_relative, width, label='HCP',
                       color='#A23B72', alpha=0.8, edgecolor='black', linewidth=1)
        bars3 = ax.bar(x + width, e_dhcp_relative, width, label='DHCP',
                       color='#F18F01', alpha=0.8, edgecolor='black', linewidth=1)

        ax.set_xlabel('Composition', fontweight='bold')
        ax.set_ylabel('Relative Energy (meV/atom)', fontweight='bold')
        ax.set_title(f'Energy of FCC, HCP, and DHCP Structures at T = {int(temperature)} K\n(Relative to FCC = 0)',
                     fontweight='bold', pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(df_plot['composition'].values, rotation=45, ha='right', fontsize=9)
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)

        # Add value labels on bars (only for non-zero values)
        for bars in [bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                if abs(height) > 5:  # Only label if > 5 meV
                    ax.text(bar.get_x() + bar.get_width() / 2., height,
                            f'{height:.0f}',
                            ha='center', va='bottom' if height > 0 else 'top',
                            fontsize=8, fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    def plot_enhanced_temperature_trends(self, compositions=None,
                                         output_dir='enhanced_temp_plots'):
        """
        Plot 2: Enhanced temperature dependence plots
        Creates individual high-quality plots for selected compositions
        """
        if self.data is None:
            print("No data loaded!")
            return

        Path(output_dir).mkdir(exist_ok=True)

        # Default compositions if none specified
        if compositions is None:
            compositions = [
                'Al00Fe00Ni100',  # Pure Ni
                'Al00Fe100Ni00',  # Pure Fe
                'Al100Fe00Ni00',  # Pure Al
                'Al33Fe34Ni33',  # Equiatomic
                'Al25Fe50Ni25',  # Ternary with negative SFE
                'Al50Fe00Ni50',  # Al-Ni binary
            ]

        for comp in compositions:
            df_comp = self.data[self.data['composition'] == comp].copy()

            if len(df_comp) == 0:
                print(f"Warning: No data for {comp}")
                continue

            # Sort by temperature
            df_comp = df_comp.sort_values('temperature')

            fig, ax = plt.subplots(figsize=(8, 6))

            temps = df_comp['temperature'].values

            # Plot with markers and error bands
            ax.plot(temps, df_comp['gamma_ISF_mJ_m2'], 'o-',
                    label='γ_ISF', linewidth=2.5, markersize=10,
                    color='#E63946', markeredgecolor='black', markeredgewidth=1)
            ax.plot(temps, df_comp['gamma_ESF_mJ_m2'], 's-',
                    label='γ_ESF', linewidth=2.5, markersize=9,
                    color='#457B9D', markeredgecolor='black', markeredgewidth=1)
            ax.plot(temps, df_comp['gamma_Twin_mJ_m2'], '^-',
                    label='γ_Twin', linewidth=2.5, markersize=9,
                    color='#2A9D8F', markeredgecolor='black', markeredgewidth=1)

            # Add zero line
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

            ax.set_xlabel('Temperature (K)', fontweight='bold', fontsize=13)
            ax.set_ylabel('Stacking Fault Energy (mJ/m²)', fontweight='bold', fontsize=13)

            # Format composition name for title
            comp_formatted = comp.replace('Al', 'Al_').replace('Fe', 'Fe_').replace('Ni', 'Ni_')
            ax.set_title(f'Temperature Dependence of SFE\n{comp_formatted}',
                         fontweight='bold', fontsize=14, pad=15)

            ax.legend(loc='best', framealpha=0.95, edgecolor='black', fontsize=11)
            ax.grid(True, alpha=0.3, linestyle='--')

            # Set x-axis to show all temperature points
            ax.set_xticks(temps)

            # Add data labels
            for i, temp in enumerate(temps):
                for sfe_type, color in [('gamma_ISF_mJ_m2', '#E63946'),
                                        ('gamma_ESF_mJ_m2', '#457B9D'),
                                        ('gamma_Twin_mJ_m2', '#2A9D8F')]:
                    value = df_comp.iloc[i][sfe_type]
                    # Only label first and last points to avoid clutter
                    if i == 0 or i == len(temps) - 1:
                        ax.text(temp, value, f'{value:.1f}',
                                fontsize=8, ha='center',
                                va='bottom' if value > 0 else 'top',
                                color=color, fontweight='bold')

            plt.tight_layout()
            output_file = Path(output_dir) / f'sfe_vs_temp_{comp}.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"  ✓ Saved: {output_file}")
            plt.close()

    def plot_composition_bars_detailed(self, temperature=400,
                                       output_file='sfe_vs_comp_detailed.png'):
        """
        Plot 3: Detailed composition bar chart with annotations
        Enhanced version of composition dependence
        """
        if self.data is None:
            print("No data loaded!")
            return

        df_temp = self.data[self.data['temperature'] == temperature].copy()
        df_temp = df_temp.sort_values('gamma_ISF_mJ_m2', ascending=False)

        fig, ax = plt.subplots(figsize=(16, 7))

        x = np.arange(len(df_temp))
        width = 0.27

        bars1 = ax.bar(x - width, df_temp['gamma_ISF_mJ_m2'], width,
                       label='γ_ISF', alpha=0.85, color='#E63946',
                       edgecolor='black', linewidth=0.8)
        bars2 = ax.bar(x, df_temp['gamma_ESF_mJ_m2'], width,
                       label='γ_ESF', alpha=0.85, color='#457B9D',
                       edgecolor='black', linewidth=0.8)
        bars3 = ax.bar(x + width, df_temp['gamma_Twin_mJ_m2'], width,
                       label='γ_Twin', alpha=0.85, color='#2A9D8F',
                       edgecolor='black', linewidth=0.8)

        ax.set_xlabel('Composition', fontweight='bold', fontsize=13)
        ax.set_ylabel('Stacking Fault Energy (mJ/m²)', fontweight='bold', fontsize=13)
        ax.set_title(f'Stacking Fault Energies Across Al-Fe-Ni Compositions at T = {int(temperature)} K',
                     fontweight='bold', fontsize=14, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(df_temp['composition'].values, rotation=45, ha='right', fontsize=8)
        ax.legend(loc='best', framealpha=0.95, edgecolor='black', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1.5, alpha=0.7)

        # Highlight extremes
        max_isf_idx = df_temp['gamma_ISF_mJ_m2'].idxmax()
        min_isf_idx = df_temp['gamma_ISF_mJ_m2'].idxmin()

        # Add annotations for max and min
        max_comp = df_temp.loc[max_isf_idx, 'composition']
        min_comp = df_temp.loc[min_isf_idx, 'composition']
        max_val = df_temp.loc[max_isf_idx, 'gamma_ISF_mJ_m2']
        min_val = df_temp.loc[min_isf_idx, 'gamma_ISF_mJ_m2']

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    def plot_pure_elements_comparison(self, output_file='pure_elements_comparison.png'):
        """
        Plot 4: Comparison of pure elements across all temperatures
        """
        if self.data is None:
            print("No data loaded!")
            return

        pure_comps = ['Al00Fe00Ni100', 'Al00Fe100Ni00', 'Al100Fe00Ni00']
        labels = ['Pure Ni', 'Pure Fe', 'Pure Al']

        df_pure = self.data[self.data['composition'].isin(pure_comps)].copy()

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        sfe_types = ['gamma_ISF_mJ_m2', 'gamma_ESF_mJ_m2', 'gamma_Twin_mJ_m2']
        sfe_labels = ['γ_ISF', 'γ_ESF', 'γ_Twin']
        colors = ['#E63946', '#457B9D', '#2A9D8F']

        for idx, (sfe_type, sfe_label, color) in enumerate(zip(sfe_types, sfe_labels, colors)):
            ax = axes[idx]

            for comp, label in zip(pure_comps, labels):
                df_comp = df_pure[df_pure['composition'] == comp].sort_values('temperature')
                ax.plot(df_comp['temperature'], df_comp[sfe_type],
                        'o-', label=label, linewidth=2.5, markersize=9,
                        markeredgecolor='black', markeredgewidth=1)

            ax.set_xlabel('Temperature (K)', fontweight='bold')
            ax.set_ylabel(f'{sfe_label} (mJ/m²)', fontweight='bold')
            ax.set_title(f'{sfe_label} for Pure Elements', fontweight='bold', pad=10)
            ax.legend(loc='best', framealpha=0.95, edgecolor='black')
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    def plot_binary_edges_analysis(self, output_file='binary_edges_analysis.png'):
        """
        Plot 5: Analysis of binary edge compositions
        """
        if self.data is None:
            print("No data loaded!")
            return

        # Define binary edges
        al_ni_edge = ['Al00Fe00Ni100', 'Al25Fe00Ni75', 'Al50Fe00Ni50',
                      'Al75Fe00Ni25', 'Al100Fe00Ni00']
        al_fe_edge = ['Al00Fe100Ni00', 'Al25Fe75Ni00', 'Al50Fe50Ni00',
                      'Al75Fe25Ni00', 'Al100Fe00Ni00']
        fe_ni_edge = ['Al00Fe00Ni100', 'Al00Fe25Ni75', 'Al00Fe50Ni50',
                      'Al00Fe75Ni25', 'Al00Fe100Ni00']

        temp = 400  # K

        fig, axes = plt.subplots(1, 3, figsize=(16, 5))

        edges = [al_ni_edge, al_fe_edge, fe_ni_edge]
        edge_names = ['Al-Ni Binary', 'Al-Fe Binary', 'Fe-Ni Binary']
        x_labels = [['Ni', '25Al', '50Al', '75Al', 'Al'],
                    ['Fe', '25Al', '50Al', '75Al', 'Al'],
                    ['Ni', '25Fe', '50Fe', '75Fe', 'Fe']]

        for idx, (edge, name, xlabels) in enumerate(zip(edges, edge_names, x_labels)):
            ax = axes[idx]

            df_edge = self.data[(self.data['composition'].isin(edge)) &
                                (self.data['temperature'] == temp)].copy()

            # Sort by composition order
            df_edge['comp_order'] = df_edge['composition'].apply(lambda x: edge.index(x))
            df_edge = df_edge.sort_values('comp_order')

            x_pos = range(len(df_edge))

            ax.plot(x_pos, df_edge['gamma_ISF_mJ_m2'], 'o-',
                    label='γ_ISF', linewidth=2.5, markersize=10, color='#E63946',
                    markeredgecolor='black', markeredgewidth=1)
            ax.plot(x_pos, df_edge['gamma_ESF_mJ_m2'], 's-',
                    label='γ_ESF', linewidth=2.5, markersize=9, color='#457B9D',
                    markeredgecolor='black', markeredgewidth=1)
            ax.plot(x_pos, df_edge['gamma_Twin_mJ_m2'], '^-',
                    label='γ_Twin', linewidth=2.5, markersize=9, color='#2A9D8F',
                    markeredgecolor='black', markeredgewidth=1)

            ax.set_xlabel('Composition', fontweight='bold')
            ax.set_ylabel('SFE (mJ/m²)', fontweight='bold')
            ax.set_title(f'{name} Edge\n(T = {temp} K)', fontweight='bold', pad=10)
            ax.set_xticks(x_pos)
            ax.set_xticklabels(xlabels, fontsize=10)
            ax.legend(loc='best', framealpha=0.95, edgecolor='black', fontsize=9)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.axhline(y=0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    def plot_sfe_correlations(self, output_file='sfe_correlations.png'):
        """
        Plot 6: Correlation between different SFE types
        """
        if self.data is None:
            print("No data loaded!")
            return

        fig, axes = plt.subplots(1, 3, figsize=(15, 5))

        # ISF vs ESF
        ax = axes[0]
        ax.scatter(self.data['gamma_ISF_mJ_m2'], self.data['gamma_ESF_mJ_m2'],
                   c=self.data['temperature'], cmap='viridis', s=60,
                   alpha=0.7, edgecolors='black', linewidth=0.5)
        ax.plot([-20, 25], [-20, 25], 'k--', alpha=0.5, label='y=x')
        ax.set_xlabel('γ_ISF (mJ/m²)', fontweight='bold')
        ax.set_ylabel('γ_ESF (mJ/m²)', fontweight='bold')
        ax.set_title('ISF vs ESF Correlation', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # ISF vs Twin
        ax = axes[1]
        ax.scatter(self.data['gamma_ISF_mJ_m2'], self.data['gamma_Twin_mJ_m2'],
                   c=self.data['temperature'], cmap='viridis', s=60,
                   alpha=0.7, edgecolors='black', linewidth=0.5)
        ax.plot([-20, 25], [-10, 12.5], 'k--', alpha=0.5, label='y=x/2')
        ax.set_xlabel('γ_ISF (mJ/m²)', fontweight='bold')
        ax.set_ylabel('γ_Twin (mJ/m²)', fontweight='bold')
        ax.set_title('ISF vs Twin Correlation', fontweight='bold')
        ax.grid(True, alpha=0.3)
        ax.legend()

        # ESF vs Twin
        ax = axes[2]
        scatter = ax.scatter(self.data['gamma_ESF_mJ_m2'], self.data['gamma_Twin_mJ_m2'],
                             c=self.data['temperature'], cmap='viridis', s=60,
                             alpha=0.7, edgecolors='black', linewidth=0.5)
        ax.set_xlabel('γ_ESF (mJ/m²)', fontweight='bold')
        ax.set_ylabel('γ_Twin (mJ/m²)', fontweight='bold')
        ax.set_title('ESF vs Twin Correlation', fontweight='bold')
        ax.grid(True, alpha=0.3)

        # Add colorbar
        cbar = plt.colorbar(scatter, ax=axes[2])
        cbar.set_label('Temperature (K)', fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✓ Saved: {output_file}")
        plt.close()

    def generate_all_additional_plots(self):
        """Generate all additional plots for the report"""
        print("\n" + "=" * 70)
        print("GENERATING ADDITIONAL PLOTS FOR REPORT")
        print("=" * 70)

        if self.data is None:
            print("Error: No data loaded!")
            return

        output_dir = Path('report_plots')
        output_dir.mkdir(exist_ok=True)

        print("\n1. Energy Comparison Plot...")
        self.plot_energy_comparison(temperature=400,
                                    output_file=output_dir / 'energy_comparison.png')

        print("\n2. Enhanced Temperature Dependence Plots...")
        self.plot_enhanced_temperature_trends(output_dir=output_dir)

        print("\n3. Detailed Composition Bar Chart...")
        self.plot_composition_bars_detailed(temperature=400,
                                            output_file=output_dir / 'sfe_vs_comp_400K.png')

        print("\n4. Pure Elements Comparison...")
        self.plot_pure_elements_comparison(output_file=output_dir / 'pure_elements_comparison.png')

        print("\n5. Binary Edges Analysis...")
        self.plot_binary_edges_analysis(output_file=output_dir / 'binary_edges_analysis.png')

        print("\n6. SFE Correlations...")
        self.plot_sfe_correlations(output_file=output_dir / 'sfe_correlations.png')

        print("\n" + "=" * 70)
        print("ALL ADDITIONAL PLOTS GENERATED!")
        print("=" * 70)
        print(f"\nPlots saved in: {output_dir}/")
        print("\nFiles generated:")
        print("  • energy_comparison.png")
        print("  • sfe_vs_temp_*.png (6 files)")
        print("  • sfe_vs_comp_400K.png")
        print("  • pure_elements_comparison.png")
        print("  • binary_edges_analysis.png")
        print("  • sfe_correlations.png")
        print("\nTotal: 11 additional plots for your report!")
        print("=" * 70 + "\n")


def main():
    """Main execution"""

    print("\n" + "=" * 70)
    print("ADDITIONAL PLOTS GENERATOR FOR MM309 ASSIGNMENT 2")
    print("=" * 70 + "\n")

    # Initialize plotter
    plotter = AdditionalSFEPlotter('sfe_results.csv')

    if plotter.data is None:
        print("\nError: Could not load data!")
        print("Make sure 'sfe_results.csv' exists in the current directory.")
        return

    # Generate all plots
    plotter.generate_all_additional_plots()


if __name__ == "__main__":
    main()
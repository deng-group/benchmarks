#!/usr/bin/env python3
"""
Script to plot VASP timing analysis results from CSV.
Generates performance comparison plots including power and price efficiency.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import yaml

# Set professional style
plt.style.use('seaborn-v0_8')
sns.set_palette('husl')
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['xtick.labelsize'] = 12
plt.rcParams['ytick.labelsize'] = 12

def load_hardware_specs(yaml_file='hardware_specs.yaml'):
    """Load hardware specifications from YAML file."""
    if not os.path.exists(yaml_file):
        print(f"YAML file {yaml_file} not found")
        return {}
    
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    
    specs = {}
    for hw, info in data.get('hardware_specs', {}).items():
        specs[hw] = {
            'power': info.get('power'),
            'price': info.get('price')
        }
    return specs

# Hardware specifications (current approximate prices as of 2025, including full system costs)
# Power in watts, Price in USD (workstation components are relatively cheap)
HARDWARE_SPECS = load_hardware_specs()

def load_data(csv_file):
    """Load the timing data from CSV."""
    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found")
        return None

    df = pd.read_csv(csv_file)

    # Filter to only include complete runs (maximum number of loops)
    max_loops = df['num_loops'].max()
    df = df[df['num_loops'] == max_loops]
    print(f"Filtered to {len(df)} complete runs (with {max_loops} loops)")

    # Extract simulation type from filename
    df['simulation_type'] = df['filename'].str.split('.').str[0]

    # Add hardware specs
    df['power_watts'] = df['hardware'].map(lambda x: HARDWARE_SPECS.get(x, {}).get('power', None))
    df['price_usd'] = df['hardware'].map(lambda x: HARDWARE_SPECS.get(x, {}).get('price', None))

    # Calculate efficiency metrics
    # Speed up relative to slowest hardware for each simulation type (higher is better)
    df['speed_up'] = 0.0
    for sim_type in df['simulation_type'].unique():
        subset = df[df['simulation_type'] == sim_type]
        max_time = subset['avg_time_per_loop'].max()
        df.loc[df['simulation_type'] == sim_type, 'speed_up'] = max_time / df['avg_time_per_loop']

    df['perf_per_watt'] = df['speed_up'] / df['power_watts']
    df['perf_per_dollar'] = df['speed_up'] / df['price_usd']

    return df

def plot_speed_up(df):
    """Plot average speed up by hardware."""
    plt.figure(figsize=(14, 8))

    # Group by hardware and calculate mean speed up
    hardware_means = df.groupby('hardware')['speed_up'].mean().sort_values(ascending=False)

    # Bar plot
    ax = hardware_means.plot(kind='bar', color='skyblue', edgecolor='black', linewidth=0.5)
    plt.title('VASP Performance Speed Up by Hardware\n(Higher is Better)', fontsize=18, fontweight='bold')
    plt.xlabel('Hardware Configuration', fontsize=14)
    plt.ylabel('Average Speed Up (relative to slowest)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('vasp_performance_speed_up.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_boxplot_by_hardware(df):
    """Box plot of speed up for each hardware."""
    plt.figure(figsize=(16, 10))

    # Sort hardware by median speed up descending
    hardware_order = df.groupby('hardware')['speed_up'].median().sort_values(ascending=False).index

    sns.boxplot(data=df, x='hardware', y='speed_up', order=hardware_order, 
                palette='viridis', linewidth=1.5, fliersize=3)
    plt.title('Distribution of VASP Performance Speed Up by Hardware\n(Higher is Better)', fontsize=18, fontweight='bold')
    plt.xlabel('Hardware Configuration', fontsize=14)
    plt.ylabel('Speed Up (relative to slowest)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('vasp_performance_boxplot.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_by_simulation_type(df):
    """Plot speed up by hardware, colored by simulation type."""
    plt.figure(figsize=(16, 10))

    # Get unique simulation types
    sim_types = df['simulation_type'].unique()

    # Create color palette
    colors = sns.color_palette('Set2', len(sim_types))
    color_dict = dict(zip(sim_types, colors))

    # Plot each simulation type
    bar_width = 0.15
    positions = range(len(df['hardware'].unique()))
    hardware_list = sorted(df['hardware'].unique(), 
                          key=lambda x: df[df['hardware']==x]['speed_up'].mean(), 
                          reverse=True)

    for i, sim_type in enumerate(sim_types):
        subset = df[df['simulation_type'] == sim_type]
        hardware_means = subset.set_index('hardware').reindex(hardware_list)['speed_up']
        plt.bar([p + i*bar_width for p in positions], hardware_means.values,
                width=bar_width, label=sim_type, alpha=0.8, color=colors[i], edgecolor='black', linewidth=0.5)

    plt.title('VASP Performance Speed Up by Hardware and Simulation Type\n(Higher is Better)', fontsize=18, fontweight='bold')
    plt.xlabel('Hardware Configuration', fontsize=14)
    plt.ylabel('Speed Up (relative to slowest)', fontsize=14)
    plt.xticks([p + bar_width*(len(sim_types)-1)/2 for p in positions], hardware_list, rotation=45, ha='right')
    plt.legend(title='Simulation Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('vasp_performance_by_type.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_performance_per_watt(df):
    """Plot speed up per watt by hardware."""
    plt.figure(figsize=(14, 8))

    # Filter out rows without power data
    df_power = df.dropna(subset=['perf_per_watt'])

    # Group by hardware and calculate mean
    hardware_means = df_power.groupby('hardware')['perf_per_watt'].mean().sort_values(ascending=False)

    # Bar plot
    ax = hardware_means.plot(kind='bar', color='green', edgecolor='black', linewidth=0.5)
    plt.title('VASP Performance per Watt by Hardware\n(Higher is Better)', fontsize=18, fontweight='bold')
    plt.xlabel('Hardware Configuration', fontsize=14)
    plt.ylabel('Speed Up per Watt (relative/W)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('vasp_performance_per_watt.png', dpi=300, bbox_inches='tight')
    plt.show()

def plot_performance_per_dollar(df):
    """Plot speed up per dollar by hardware."""
    plt.figure(figsize=(14, 8))

    # Filter out rows without price data
    df_price = df.dropna(subset=['perf_per_dollar'])

    # Group by hardware and calculate mean
    hardware_means = df_price.groupby('hardware')['perf_per_dollar'].mean().sort_values(ascending=False)

    # Bar plot
    ax = hardware_means.plot(kind='bar', color='blue', edgecolor='black', linewidth=0.5)
    plt.title('VASP Performance per Dollar by Hardware\n(Higher is Better)', fontsize=18, fontweight='bold')
    plt.xlabel('Hardware Configuration', fontsize=14)
    plt.ylabel('Speed Up per Dollar (relative/$)', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.savefig('vasp_performance_per_dollar.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    csv_file = 'vasp_timing_analysis.csv'

    df = load_data(csv_file)
    if df is None:
        return

    print(f"Loaded {len(df)} data points from {csv_file}")
    print(f"Hardware configurations: {df['hardware'].nunique()}")
    print(f"Simulation types: {df['simulation_type'].unique()}")

    # Generate plots
    plot_speed_up(df)
    plot_boxplot_by_hardware(df)
    plot_by_simulation_type(df)
    plot_performance_per_watt(df)
    plot_performance_per_dollar(df)

    print("Plots saved as PNG files:")
    print("- vasp_performance_speed_up.png")
    print("- vasp_performance_boxplot.png")
    print("- vasp_performance_by_type.png")
    print("- vasp_performance_per_watt.png")
    print("- vasp_performance_per_dollar.png")

if __name__ == '__main__':
    main()
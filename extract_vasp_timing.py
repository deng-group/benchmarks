#!/usr/bin/env python3
"""
Script to extract VASP computational timing data from gzipped OUTCAR files.
Sums CPU times from LOOP lines to get total computational time, excluding initialization.
"""

import gzip
import os
import re
from pathlib import Path

def extract_timing_from_outcar(filepath):
    """
    Extract timing data from a gzipped OUTCAR file.
    Returns: total_real_time, num_loops
    """
    total_real_time = 0.0
    num_loops = 0

    try:
        with gzip.open(filepath, 'rt', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Look for LOOP timing lines
                if 'LOOP:' in line:
                    # Extract real time: " LOOP:  cpu time   123.456: real time   124.567"
                    match = re.search(r'real time\s+(\d+\.\d+)', line)
                    if match:
                        real_time = float(match.group(1))
                        total_real_time += real_time
                        num_loops += 1
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0.0, 0

    return total_real_time, num_loops

def parse_hardware_from_filename(filename):
    """
    Parse hardware identifier from filename.
    Examples:
    - large_spin_2DPerovskites.9654_4090.gz -> 9654_4090
    - large_spin_2DPerovskites.genoa_64cores.gz -> genoa_64cores
    """
    # Remove .gz extension
    name = filename.replace('.gz', '')
    # Split by . and take the last part before .gz
    parts = name.split('.')
    if len(parts) >= 2:
        return parts[-1]
    return 'unknown'

def main():
    outcars_dir = Path('VASP/outcars')
    if not outcars_dir.exists():
        print(f"Directory {outcars_dir} not found")
        return

    results = []

    # Process all .gz files
    for gz_file in outcars_dir.glob('*.gz'):
        print(f"Processing {gz_file.name}...")
        total_real_time, num_loops = extract_timing_from_outcar(gz_file)
        hardware = parse_hardware_from_filename(gz_file.name)

        if num_loops > 0:
            avg_time_per_loop = total_real_time / num_loops
        else:
            avg_time_per_loop = 0.0

        results.append({
            'filename': gz_file.name,
            'hardware': hardware,
            'total_real_time': total_real_time,
            'num_loops': num_loops,
            'avg_time_per_loop': avg_time_per_loop
        })

    # Sort by hardware
    results.sort(key=lambda x: x['hardware'])

    # Print results
    print("\nVASP Performance Analysis Results:")
    print("=" * 80)
    print(f"{'Hardware':<20} {'Total Real Time (s)':<18} {'Num Loops':<10} {'Avg Time/Loop (s)':<18}")
    print("-" * 80)

    current_hardware = None
    for result in results:
        if result['hardware'] != current_hardware:
            if current_hardware is not None:
                print()  # Blank line between hardware groups
            current_hardware = result['hardware']

        print(f"{result['hardware']:<20} {result['total_real_time']:<18.3f} {result['num_loops']:<10} {result['avg_time_per_loop']:<18.3f}")

    # Save to CSV for further analysis
    import csv
    with open('vasp_timing_analysis.csv', 'w', newline='') as csvfile:
        fieldnames = ['filename', 'hardware', 'total_real_time', 'num_loops', 'avg_time_per_loop']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to vasp_timing_analysis.csv")

if __name__ == '__main__':
    main()
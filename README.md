# benchmarks

Benchmark suite for VASP and MACE ML potentials across hardware configurations.

## Structure

```
benchmarks/
├── VASP/                    # VASP benchmarks
│   ├── run_vasp.sh          # Run VASP on all test systems
│   ├── clean.sh             # Clean VASP output files
│   ├── outcars/             # Collected OUTCAR files (gzipped)
│   ├── large_spin_2DPerovskites/
│   ├── medium_hse_LLZO/
│   ├── medium_surface_PdSe/
│   ├── small_nospin_NZSP/
│   └── small_spin_NVP/
├── MACE/                    # MACE benchmark scripts
│   ├── run_mace_md.py       # MD inference benchmark
│   ├── run_md.sh            # Run MD benchmark
│   ├── run_train.sh         # Run training benchmark
│   └── database/            # Training data
├── extract_vasp_timing.py   # Extract timing from OUTCAR files
├── plot_vasp_timing.py      # Generate performance comparison plots
├── hardware_specs.yaml      # Hardware specifications (power, price)
└── Makefile                 # Convenience targets
```

## Usage

### VASP Benchmarks

```bash
# Run VASP benchmarks
make vasp

# Extract timing data from OUTCARs
python extract_vasp_timing.py

# Generate plots
python plot_vasp_timing.py
```

### MACE Benchmarks

```bash
# MD inference benchmark
make mace_md

# Training benchmark
make mace_train
```

## Hardware Coverage

- AMD EPYC 9654 (single/dual, with GPU)
- AMD Genoa 9354 (single/dual)
- AMD EPYC 7742 (Milan)
- Intel Xeon 8452Y
- Intel 13900K/14900K workstations
- GPUs: RTX 4090, RTX 5090, A6000, V100

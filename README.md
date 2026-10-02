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

## Related: cluster time-vs-cost benchmark (Oct 2026)

The same VASP 6.5.1 and MACE-MPA-0 MD workloads were run on every partition available to the group —
NUS **vanda** and **hopper**, **China HPC** (超算云平台, Inner Mongolia 2) and **fornax** — and plotted as
wall time against cost per job, so the Pareto-optimal nodes (nothing is both faster and cheaper) stand out.

![Time–cost Pareto front](https://raw.githubusercontent.com/LIMENGKE24/hpc-benchmark/main/analysis/pareto.png)

- **VASP** (128-atom Na₃PS₄, 25 SCF steps): fastest = fornax EPYC 9354 node (104 s); cheapest = one China HPC V100 (138 s, 0.007 SGD/job).
- **MACE MD** (1,024 / 3,456 atoms): fastest = fornax RTX 5090; cheapest = China HPC V100; H100/H200 match the RTX 5090 on speed at ~5× the cost per ns.

Inputs, job scripts, per-run records, the cost model with sources, and a node-fault report for fornax
(`c15`, `g01`) are in **[LIMENGKE24/hpc-benchmark](https://github.com/LIMENGKE24/hpc-benchmark)**.
Note that fornax prices there are a public-cloud rental proxy (fornax has no chargeback), unlike the purchase
prices used in `hardware_specs.yaml` here.

# benchmarks
Benchmarks

## Running benchmarks
### MACE
- MD (inference): `make mace_md`, you should set `$machine_config` in your environment. (machine_config is just a name of this benchmark)
- Training: `make mace_train`, you should set `$machine_config` and `$device` in your environment. (device is `cuda` or `cpu`)

### VASP
- `make vasp`, you should set `$machine_config` and `$nproc` in your environment. (nproc is number of CPU cores/GPU)
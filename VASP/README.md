## Test configurations

- `genoa_96cores_9654_single`: Test run on 9654 single CPU with 12x16GB 4800Mhz DDR5, openmpi+openblas+scalapack+fftw3 compiler stack (OHPC)
- `genoa_96cores_9654_task64_single`: Test run on 9654 single CPU with 12x16GB 4800Mhz DDR5, using 64 MPI ranks, openmpi+openblas+scalapack+fftw3 compiler stack (OHPC)
- `9654_192core_gnu`: Test run with dual EPYC 9654 CPU with (OHPC) gnu14 stack
- `9654_192core_mkl`: Test run with dual EPYC 9654 CPU with (OHPC) mkl stack
- `9354_4090`: Test run with a single RTX 4090 (48G) card with EPYC 9354 processor (one core per MPI rank) using nvhpc 25 stack
- `9354_A6000`: Test run with a single RTX A6000 (48G) card with EPYC 9354 processor (one core per MPI rank) using nvhpc 25 stack
- `9354_4090_x2`: Test run with a two 4090 (48G) card with EPYC 9354 processor (one core per MPI rank), interconnect is done via a PCIE-bridge using nhhpc 25 stack

## Note

The NCORE value affects the HSE06 test a lot, so the results should be treated with care.



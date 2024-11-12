#!/bin/bash
machine_config='RTX4090'

for float in float32 float64; do
    seed=1234
    python -u run_mace_md.py $float $seed > run_md_${machine_config}_${float}_${seed}.log
done

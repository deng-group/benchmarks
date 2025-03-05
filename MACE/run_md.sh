#!/bin/bash
machine_config=$1
device=$2

for float in float32 float64; do
    seed=1234
    python -u run_mace_md.py --dtype $float --seed $seed --device $device > benchmark_results/run_md_${machine_config}_${float}_${seed}.log
    git add benchmark_results/run_md_${machine_config}_${float}_${seed}.log
    git commit -m "Add benchmark results for run_md_${machine_config}_${float}_${seed}.log"
done

git push

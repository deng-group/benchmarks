#!/bin/bash
machine_config=$1
git config --global user.name "container"
git config --global user.email "container@container.com"
for float in float32 float64; do
    seed=1234
    python -u run_mace_md.py $float $seed > benchmark_results/run_md_${machine_config}_${float}_${seed}.log
    git add benchmark_results/run_md_${machine_config}_${float}_${seed}.log
    git commit -m "Add benchmark results for run_md_${machine_config}_${float}_${seed}.log"
done

git push

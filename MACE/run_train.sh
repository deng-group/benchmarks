#!/bin/bash
git config --global user.name "container"
git config --global user.email "container@container.com"
# Try download the model if it doesn't exist
# file_name="mace_agnesi_medium.model"
# url="https://github.com/ACEsuit/mace-mp/releases/download/mace_mp_0b/mace_agnesi_medium.model"

# # Check if the file exists
# if [[ ! -f "$file_name" ]]; then
#     echo "$file_name does not exist. Downloading..."
#     # Use wget to download the file
#     if command -v wget > /dev/null; then
#         wget "$url" -O "$file_name"
#     # Use curl if wget is not available
#     elif command -v curl > /dev/null; then
#         curl -L "$url" -o "$file_name"
#     else
#         echo "Neither wget nor curl is installed. Cannot download the file."
#         exit 1
#     fi
    
#     # Check if the download was successful
#     if [[ -f "$file_name" ]]; then
#         echo "$file_name has been downloaded successfully."
#     else
#         echo "Failed to download $file_name."
#     fi
# else
#     echo "$file_name already exists."
# fi

name="LPGSO"
seed=1234
device=$2
max_num_epochs=5
machine_config=$1

mace_run_train \
    --name="$name"\
    --foundation_model="mace_agnesi_medium.model"\
    --train_file="./database/$name.xyz" \
    --valid_fraction=0.1\
    --energy_weight=1 \
    --forces_weight=10 \
    --compute_stress=True \
    --stress_weight=1 \
    --stress_key='stress' \
    --swa \
    --swa_forces_weight=100\
    --E0s="{32:-13.928397,3:-0.40914546,8:-0.62290835,15:-4.5251547,16:-5.1361696}"\
    --model="MACE" \
    --scaling='rms_forces_scaling' \
    --lr=0.01 \
    --ema \
    --ema_decay=0.99 \
    --batch_size=24 \
    --max_num_epochs=$max_num_epochs \
    --amsgrad \
    --device="$device" \
    --seed=$seed \
    --scheduler_patience=5 \
    --patience=50 \
    --default_dtype="${dtype}" > train_${machine_config}_${name}_${dtype}_${seed}.log
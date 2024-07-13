#!/bin/bash
# Set job requirements
#SBATCH --job-name=Snellius_example_project
#SBATCH --partition=rome
#SBATCH --nodes=1
#SBATCH --ntasks=128
#SBATCH --time=00:10:40
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=joost.berkhout@vu.nl
#SBATCH --output="slurm-%j.out"

# Create some variables
base_dir="$HOME/Snellius example project"
results_folder="$base_dir/$(date +"results %d-%m-%Y %H-%M-%S")"
experiments_settings="$base_dir/experiments_settings.json"

# Move to working directory and create results folder
cd "$base_dir"
mkdir -p "$results_folder"

instances=$(jq -r '.instances[]' "$experiments_settings")
methods=$(jq -r '."methods"[]' "$experiments_settings")

while read -r instance; do
    while read -r method; do
        srun --ntasks=1 --nodes=1 --cpus-per-task=1 poetry run python "$base_dir/run_experiment.py" "$instance" "$method" "$results_folder" &
    done <<< "$methods"
done <<< "$instances"
wait

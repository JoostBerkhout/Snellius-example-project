"""Creates a Snellius job script file based on experiments settings. """

import json

from constants import (
    EMAIL,
    EST_SEC_PER_TASK,
    EXPERIMENTS_SETTINGS_NAME,
    JOB_SCRIPT_NAME,
    MAX_CORES_PER_NODE,
    PARTITION_NAME,
)

# get project name by looking up the name of grandfather folder
project_name = __file__.split("\\")[-3]

# load experiments settings
with open(f"../{EXPERIMENTS_SETTINGS_NAME}") as f:
    settings = json.load(f)

# calculate number of tasks
num_tasks = min(
    len(settings["methods"]) * len(settings["instances"]), MAX_CORES_PER_NODE
)

# estimate total time required
est_total_time_secs = EST_SEC_PER_TASK * num_tasks  # in seconds
hours = est_total_time_secs // 3600
minutes = (est_total_time_secs % 3600) // 60
seconds = est_total_time_secs % 60
total_time_format = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

# Job script template
args = (
    '"$base_dir/run_experiment.py" "$instance" ' '"$method" "$results_folder"'
)
job_script_template = f"""#!/bin/bash
# Set job requirements
#SBATCH --job-name={project_name.replace(' ', '_')}
#SBATCH --partition={PARTITION_NAME}
#SBATCH --nodes=1
#SBATCH --ntasks={num_tasks}
#SBATCH --time={total_time_format}
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user={EMAIL}

# Create some variables
base_dir="$HOME/{project_name}"
results_folder="$base_dir/$(date +"results %d-%m-%Y %H-%M-%S")"
experiments_settings="$base_dir/{EXPERIMENTS_SETTINGS_NAME}"

# Move to base directory and create results folder
cd "$base_dir"
mkdir -p "$results_folder"

instances=$(jq -r '.instances[]' "$experiments_settings")
methods=$(jq -r '."methods"[]' "$experiments_settings")

while read -r instance; do
    while read -r method; do
        srun --ntasks=1 --nodes=1 --cpus-per-task=1 poetry run python {args} &
    done <<< "$methods"
done <<< "$instances"
wait
"""

# Write job script to file
with open(f"../{JOB_SCRIPT_NAME}", "w", newline="\n") as f:
    f.write(job_script_template)

print(f"Job script stored in ../{JOB_SCRIPT_NAME}")

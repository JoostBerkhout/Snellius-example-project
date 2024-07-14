# Snellius example project

In this example project you find a way to conduct experiments on Snellius 
of the following type: We have different (problem) instances on which we 
want to try different methods. In particular, for each instance we want to 
run each method and store the results. All experiment runs are independent 
of each other, so we can run them in parallel. 

The idea is that this code can be used as a simple template for conducting 
experiments on Snellius. It stores the used .sh script and experiment 
settings in the results folder for reproducibility.

## Overview of project structure

The project structure is as follows:

- `Snellius setup\\`: Folder with scripts to set up the experiments on Snellius.
- `src\\`: Folder with project source code to be run on Snellius.
- `experiments_settings.json`: Contains the settings of the experiments.
- `job_script_Snellius.sh`: Contains the job script to run the experiments 
  on Snellius.
- `run_experiment.py`: Contains the code to run each experiment in parallel.
- `README.md`: Contains the documentation of the project.

## What steps are needed to run the experiments?

The steps to run the experiments are as follows:

1. Create an `experiments_settings.json` file with the experiments settings 
   in the project's root folder. To that end, one can use `Snellius 
   setup\experiments_settings_constructor.py` which will create 
   `experiments_settings.json` in the project's root folder. Alternatively, one 
   can create `experiments_settings.json` manually. But I think it is most 
   convenient to change `Snellius
   setup\experiments_settings_constructor.py` to your needs and run it.
2. Create a `job_script_Snellius.sh` job script file in the project's root 
   folder. To that end, one can use `Snellius setup\job_script_constructor.
   py`. Alternatively, one can create `job_script_Snellius.sh` manually. 
   Important: there should be an `experiments_settings.json` file in the 
   same folder as `job_script_Snellius.sh` (so perform first step 1). 
3. Place your code in the `src` folder and ensure `run_experiment.py` has 
   correct access to it. 
4. It is a good idea to test the code locally regarding `run_experiment.py` 
   (just give some dummy arguments for testing). For example, you could run 
   `run_experiment.py "instance 1" "amazing method 2" results\` to see 
   whether it correctly creates a `.json` file in `results//instance 1//amazing 
   method 2//results.json`.
5. Copy the project to Snellius and navigate to the project's root folder. 
   Ensure that poetry is installed on Snellius and run `poetry install` in 
   case the project does not have an own environment yet. You might get an 
   error when running `poetry install` that states: ``Additional properties 
   are not allowed ('package-mode' was unexpected)''. In that case, comment 
   the line `package-mode = true` in the `pyproject.toml` file, remove the 
   lock file and run `poetry install` again.
6. Run the job script `job_script_Snellius.sh` on Snellius using command 
   `sbatch job_script_Snellius.sh` (ensure that you are in the root folder 
   of the project). 
7. The results will be stored in a folder (by default named `results` with a 
   timestamp in the root folder).

## Appendix: Explaination of the job script's main idea

### Line-by-line Explanation of the Shell Script

Here's a detailed explanation of the provided shell script:

```
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
```

### Line-by-line Breakdown

```markdown
```bash
#!/bin/bash
```
- This line specifies the script should be run using the Bash shell.

```bash
# Set job requirements
#SBATCH --job-name=Snellius_example_project
```
- Specifies the name of the job as `Snellius_example_project`.

```bash
#SBATCH --partition=rome
```
- Specifies the partition (queue) to submit the job to, in this case, `rome`.

```bash
#SBATCH --nodes=1
```
- Requests 1 compute node for the job.

```bash
#SBATCH --ntasks=128
```
- Requests 128 tasks for the job, usually corresponding to the number of CPU cores.

```bash
#SBATCH --time=00:10:40
```
- Sets a time limit of 10 minutes and 40 seconds for the job.

```bash
#SBATCH --mail-type=BEGIN,END
```
- Requests email notifications when the job begins and ends.

```bash
#SBATCH --mail-user=joost.berkhout@vu.nl
```
- Specifies the email address to send notifications to.

```bash
#SBATCH --output="slurm-%j.out"
```
- Sets the name of the output file for the job's standard output, where `%j` is replaced by the job ID.

```bash
# Create some variables
base_dir="$HOME/Snellius example project"
results_folder="$base_dir/$(date +"results %d-%m-%Y %H-%M-%S")"
experiments_settings="$base_dir/experiments_settings.json"
```
- Defines variables: `base_dir` for the project's base directory, `results_folder` for the results directory with a timestamp, and `experiments_settings` for the path to the JSON settings file.

```bash
# Move to working directory and create results folder
cd "$base_dir"
mkdir -p "$results_folder"
```
- Changes the current directory to `base_dir` and creates the `results_folder` if it doesn't exist.

```bash
instances=$(jq -r '.instances[]' "$experiments_settings")
methods=$(jq -r '."methods"[]' "$experiments_settings")
```
- Uses `jq` to parse `experiments_settings.json` and extract lists of instances and methods.

```bash
while read -r instance; do
    while read -r method; do
        srun --ntasks=1 --nodes=1 --cpus-per-task=1 poetry run python "$base_dir/run_experiment.py" "$instance" "$method" "$results_folder" &
    done <<< "$methods"
done <<< "$instances"
wait
```
- Iterates over each instance and method, running `run_experiment.py` with `srun` in parallel for each combination. The `wait` command ensures the script waits for all background tasks to complete before finishing.


### Explanation of the Flow

1. The script sets up the job requirements and defines necessary variables.
2. It uses `jq` to extract the `instances` and `methods` arrays from the JSON file.
3. The script starts the outer `while` loop, iterating over each `instance`.
4. For each `instance`, it starts the inner `while` loop, iterating over each `method`.
5. For each pair of `instance` and `method`, it runs the experiment.
6. The nested loops ensure that every combination of `instance` and `method` is processed.
7. The script prints "End test" after processing all combinations.

# Snellius example project

In this example project you find a way to conduct experiments on Snellius 
of the following type: We have different (problem) instances on which we 
want to try different methods (if one wants to apply the same method with 
different settings, then just add extra methods with these different settings).
In particular, for each instance we want to run each method and store the 
results. All experiment runs are independent of each other, so we can run them 
in parallel. The idea is that this code can be used as a template for conducting
experiments on Snellius.

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
   can create `experiments_settings.json` manually.
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
   case the project does not have an own environment yet. 
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
#SBATCH --job-name=Snellius_design
#SBATCH --nodes=1
#SBATCH --ntasks=9
#SBATCH --time=00:07:12
#SBATCH --mail-type=BEGIN,END
#SBATCH --mail-user=joost.berkhout@vu.nl

# Create some variables
base_dir="$HOME/Snellius design"
results_folder="$base_dir/$(date +"Results %d-%m-%Y %H-%M-%S")"
experiments_settings="$base_dir/experiments_settings.json"
instances=$(jq -r '.instances[]' "$experiments_settings")
methods=$(jq -r '."methods"[]' "$experiments_settings")

echo "Start test"
while read -r instance; do
    while read -r method; do
        echo "$instance"
        echo "$method"
    done <<< "$methods"
done <<< "$instances"
echo "End test"
```

### Line-by-line Breakdown

1. **`#!/bin/bash`**
    - Shebang line indicating that the script should be run using the Bash shell.

2. **`# Set job requirements`**
    - A comment explaining that the following lines set job requirements.

3. **`#SBATCH --job-name=Snellius_design`**
    - Sets the name of the job to "Snellius_design".

4. **`#SBATCH --nodes=1`**
    - Requests 1 node for the job.

5. **`#SBATCH --ntasks=9`**
    - Requests 9 tasks for the job.

6. **`#SBATCH --time=00:07:12`**
    - Sets the maximum runtime of the job to 7 minutes and 12 seconds.

7. **`#SBATCH --mail-type=BEGIN,END`**
    - Requests email notifications when the job begins and ends.

8. **`#SBATCH --mail-user=joost.berkhout@vu.nl`**
    - Sets the email address for job notifications.

9. **`# Create some variables`**
    - A comment indicating the start of variable definitions.

10. **`base_dir="$HOME/Snellius design"`**
    - Sets the base directory to the "Snellius design" folder in the user's home directory.

11. **`results_folder="$base_dir/$(date +"Results %d-%m-%Y %H-%M-%S")"`**
    - Sets the results folder path, including a timestamp.

12. **`experiments_settings="$base_dir/experiments_settings.json"`**
    - Sets the path to the `experiments_settings.json` file.

13. **`instances=$(jq -r '.instances[]' "$experiments_settings")`**
    - Uses `jq` to extract each element from the `instances` array in the JSON file and assigns them to the `instances` variable.

14. **`methods=$(jq -r '."methods"[]' "$experiments_settings")`**
    - Uses `jq` to extract each element from the `"methods"` array in the JSON file and assigns them to the `methods` variable.

15. **`echo "Start test"`**
    - Prints "Start test" to the console.

16. **`while read -r instance; do`**
    - Starts a `while` loop that reads each line of the `instances` variable one by one, assigning the current line to the variable `instance`.
    - **`read -r`**: Reads a line of input, preserving the backslashes (using `-r`).

17. **`    while read -r method; do`**
    - Inside the first `while` loop, starts another `while` loop that reads each line of the `methods` variable one by one, assigning the current line to the variable `method`.

18. **`        echo "$instance"`**
    - Inside the nested `while` loop, prints the current `instance`.

19. **`        echo "$method"`**
    - Inside the nested `while` loop, prints the current `method`.

20. **`    done <<< "$methods"`**
    - Feeds the contents of the `methods` variable to the inner `while` loop using here-strings.

21. **`done <<< "$instances"`**
    - Feeds the contents of the `instances` variable to the outer `while` loop using here-strings.

22. **`echo "End test"`**
    - Prints "End test" to the console.

### Explanation of the Flow

1. The script sets up the job requirements and defines necessary variables.
2. It uses `jq` to extract the `instances` and `methods` arrays from the JSON file.
3. The script starts the outer `while` loop, iterating over each `instance`.
4. For each `instance`, it starts the inner `while` loop, iterating over each `method`.
5. For each pair of `instance` and `method`, it prints their values.
6. The nested loops ensure that every combination of `instance` and `method` is processed.
7. The script prints "End test" after processing all combinations.

### Expected Output

Given that there are 3 instances and 3 methods, the script will print the combination of each instance and method, resulting in 9 pairs:

```
Start test
instance 1
method 1
instance 1
method 2 1
instance 1
method 3
instance 2
method 1
instance 2
method 2 1
instance 2
method 3
instance 3
method 1
instance 3
method 2 1
instance 3
method 3
End test
```

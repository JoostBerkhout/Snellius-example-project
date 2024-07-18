# ruff: noqa: E402
import argparse
import json
import os
import sys
import time

# add the 'src' directory to the PYTHONPATH first (ugly, but ensures you can
# directly import modules within the 'src' directory directly, i.e.,
# `import module_name` instead of import `src.module_name`; easy when copying
# existing code into src directory and running it from there)
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
sys.path.insert(0, src_dir)

from src.instances import MAPPING_INSTANCES
from src.methods import MAPPING_METHODS
from src.run_method import run_method


def run_experiment(instance, method, settings, results_loc, verbose=True):
    """
    Runs experiment for instance with method and given settings.

    Parameters
    ----------
    instance : str
        Name of the problem instance.
    method : str
        Name of the method.
    settings : dict
        Dictionary with settings.
    results_loc : str
        Path to the folder where the experiment results should be stored.
    verbose : bool
        If True, print progress (including some timing for experimentation).

    Returns
    -------
    None

    """

    if verbose:
        start_time = time.time()
        print(f"Running experiment for {instance} with {method}")

    # init
    results = []
    instance_fun = MAPPING_INSTANCES[instance]
    method_fun = MAPPING_METHODS[method]

    # run the method # repetitions times (for illustrative purposes)
    for seed in range(settings["# repetitions"]):
        result = run_method(instance_fun(seed), method_fun, settings)
        results.append(result)

    if verbose:
        start_time_saving = time.time()

    # save results in a folder results_loc\method\problem_instance
    results_folder = os.path.join(results_loc, method, instance)
    os.makedirs(results_folder, exist_ok=True)
    results_path = os.path.join(results_folder, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=4)

    if verbose:
        # print durations
        cur_time = time.time()
        duration = cur_time - start_time
        duration_saving = cur_time - start_time_saving
        print(
            f"Experiment for {instance} with {method} took {duration:.4f} secs"
            f" (saving took {duration_saving:.4f} secs)"
        )


def parse_arguments():
    """Parse the arguments for the script."""

    # initialize the parser
    parser = argparse.ArgumentParser(
        description="Run an experiment with the specified instance and method, "
        "saving the results in the specified folder. Ensure that "
        "there is a single JSON file in the current folder with "
        "experiment settings."
    )

    # add arguments
    parser.add_argument(
        "instance_name",
        type=str,
        help="Name of the instance to use for the experiment.",
    )
    parser.add_argument(
        "method_name",
        type=str,
        help="Name of the method to apply in the experiment.",
    )
    parser.add_argument(
        "results_folder",
        type=str,
        help="Folder to save the results of the experiment.",
    )

    return parser.parse_args()


def main():

    # parse the arguments
    args = parse_arguments()

    # assign the parsed arguments to variables
    instance = args.instance_name
    method = args.method_name
    results_folder = args.results_folder

    # create results directory if it does not exist
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    # find all json files in current folder
    json_files = [f for f in os.listdir(".") if f.endswith(".json")]
    assert len(json_files) == 1, "Only one json file in the current folder"
    experiments_settings_name = json_files[0]

    # load experiments settings
    with open(experiments_settings_name, "r") as f:
        settings = json.load(f)

    # save experiments settings in the results folder
    name = "log_" + experiments_settings_name
    with open(os.path.join(results_folder, name), "w") as f:
        json.dump(settings, f, indent=4)

    # find all .sh files in current folder
    sh_files = [f for f in os.listdir(".") if f.endswith(".sh")]
    assert len(sh_files) == 1, "Ensure that only 1 sh file is in current folder"
    job_script_name = sh_files[0]

    # save a copy of .sh file in the results folder
    job_script_path = os.path.join(results_folder, "log_" + job_script_name)
    with open(job_script_path, "w") as f, open(job_script_name, "r") as f_templ:
        f.write(f_templ.read())

    # run experiment
    run_experiment(instance, method, settings, results_folder)


if __name__ == "__main__":
    main()

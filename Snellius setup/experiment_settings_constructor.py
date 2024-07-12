"""Creates an experiments_settings.json file with the experiments settings. """

import json

from constants import EXPERIMENTS_SETTINGS_NAME, JOB_SCRIPT_NAME

# set general experiments settings
# ================================

json_dict = {
    "# repetitions": 3,
    "generic parameter 1": 4000,
    "generic parameter 2": 20,
    "generic parameter 3": 23,
    "methods": [],
    "instances": [],
}

# methods to compare
# ==================

num_methods = 10
json_dict["methods"] = [f"method {i + 1}" for i in range(num_methods)]

# instances to consider
# =====================

num_instance = 13
json_dict["instances"] = [f"instance {i + 1}" for i in range(num_instance)]

# store json file as experiments_settings.json
# ==========================================
file_loc = f"../{EXPERIMENTS_SETTINGS_NAME}"
with open(file_loc, "w") as f:
    json.dump(json_dict, f, indent=4)

print(
    f"Experiments settings stored in {file_loc} (do not forget to run "
    f"{JOB_SCRIPT_NAME} to create the job script)"
)

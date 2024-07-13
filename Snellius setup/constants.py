EXPERIMENTS_SETTINGS_NAME = "experiments_settings.json"
JOB_SCRIPT_NAME = "job_script_Snellius.sh"
EMAIL = "joost.berkhout@vu.nl"
EST_SEC_PER_TASK = 5.0
PARTITION_NAME = "rome"
MAX_CORES_PER_NODE = 128
USE_SCRATCH = False  # if True, use $TMPDIR as storage
PYTHON_CMD = "python3.9"  # executable to run python scripts in poetry (used
# when USE_SCRATCH is True because then it does not find the correct python
# version automatically anymore [I guess due to the copying])

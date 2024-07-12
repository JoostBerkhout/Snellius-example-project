def fun_for_instance(name):
    def dummy_fun_for_instance(seed):
        return f"{name} function call for seed {seed}"

    return dummy_fun_for_instance


MAPPING_INSTANCES = {
    f"instance {i}": fun_for_instance(f"instance {i}") for i in range(100)
}

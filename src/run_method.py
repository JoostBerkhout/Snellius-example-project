from typing import Callable


def run_method(instance: str, method: Callable, settings: dict) -> dict:
    # Runs the method on the instance with the given settings.

    return {
        "instance": instance,
        "method": method(),
        "# repetitions": settings["# repetitions"],
        "generic parameter 1": settings["generic parameter 1"],
        "generic parameter 2": settings["generic parameter 2"],
        "generic parameter 3": settings["generic parameter 3"],
    }

from pathlib import Path

from performance_lab.execution import Execution
from performance_lab.runner import Runner


def run(target_file: str | Path) -> Execution:
    """Run a Python program and return its complete execution analysis."""
    result = Runner(target_file).run()
    return Execution.from_result(result)
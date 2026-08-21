import subprocess
import sys
from pathlib import Path


class Runner:
    def __init__(self, target_file: str | Path) -> None:
        self.target_file = Path(target_file).resolve()

    def run(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.target_file)],
            capture_output=True,
            text=True,
            check=False,
        )
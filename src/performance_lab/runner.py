import json
import subprocess
import sys
from pathlib import Path

from performance_lab.events import EventType, ExecutionEvent


class Runner:
    def __init__(self, target_file: str | Path) -> None:
        self.target_file = Path(target_file).resolve()

    def run(self) -> list[ExecutionEvent]:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "performance_lab.bootstrap",
                str(self.target_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Target program failed with exit code {result.returncode}:\n"
                f"{result.stdout}\n"
                f"{result.stderr}"
            )

        events: list[ExecutionEvent] = []

        for line in result.stderr.splitlines():
            if not line.strip():
                continue

            data = json.loads(line)

            events.append(
                ExecutionEvent(
                    event_type=EventType(data["event_type"]),
                    timestamp=data["timestamp"],
                    file=data["file"],
                    line=data["line"],
                    function=data["function"],
                    data=data["data"],
                )
            )

        return events
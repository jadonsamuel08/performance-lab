import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from performance_lab.events import EventType, ExecutionEvent


@dataclass
class RunResult:
    process: subprocess.CompletedProcess[str]
    events: list[ExecutionEvent]


class Runner:
    def __init__(self, target_file: str | Path) -> None:
        self.target_file = Path(target_file).resolve()

    def run(self) -> RunResult:
        process = subprocess.run(
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

        events = [
            self._deserialize_event(line)
            for line in process.stderr.splitlines()
            if line.strip()
        ]

        return RunResult(
            process=process,
            events=events,
        )

    @staticmethod
    def _deserialize_event(line: str) -> ExecutionEvent:
        data = json.loads(line)

        return ExecutionEvent(
            event_type=EventType(data["event_type"]),
            timestamp=data["timestamp"],
            file=data["file"],
            line=data["line"],
            function=data["function"],
            data=data["data"],
        )
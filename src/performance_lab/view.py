from dataclasses import dataclass
from pathlib import Path

from performance_lab.events import ExecutionEvent
from performance_lab.execution import Execution


@dataclass(frozen=True)
class ExecutionView:
    """Represents what the digital microscope currently shows."""

    event: ExecutionEvent | None
    file: str | None
    line: int | None
    function: str | None
    state: dict[str, object]
    call_stack: list[str]
    position: int
    total_events: int

    @property
    def progress(self) -> float:
        if self.total_events == 0:
            return 0.0

        if self.position < 0:
            return 0.0

        return (self.position + 1) / self.total_events

    @classmethod
    def from_execution(cls, execution: Execution) -> "ExecutionView":
        recorder = execution.recorder
        event = recorder.current

        if event is None:
            return cls(
                event=None,
                file=None,
                line=None,
                function=None,
                state={},
                call_stack=[],
                position=recorder.position,
                total_events=len(execution.events),
            )

        return cls(
            event=event,
            file=_display_path(event.file),
            line=event.line,
            function=event.function,
            state=recorder.state.snapshot(),
            call_stack=_build_call_stack(
                execution.events,
                recorder.position,
            ),
            position=recorder.position,
            total_events=len(execution.events),
        )


def _build_call_stack(
    events: list[ExecutionEvent],
    position: int,
) -> list[str]:
    stack: list[str] = []

    for event in events[: position + 1]:
        if event.event_type.value == "function_call":
            stack.append(event.function)

        elif event.event_type.value == "function_return":
            if stack:
                stack.pop()

    return stack


def _display_path(path: str) -> str:
    try:
        relative_path = (
            Path(path)
            .resolve()
            .relative_to(Path.cwd().resolve())
        )
        return relative_path.as_posix()
    except ValueError:
        return Path(path).as_posix()
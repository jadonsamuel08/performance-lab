from dataclasses import dataclass

from performance_lab.events import ExecutionEvent
from performance_lab.execution import Execution
from performance_lab.source import SourceLine, SourceViewer


@dataclass(frozen=True)
class ExecutionView:
    """Represents what the digital microscope currently shows."""

    event: ExecutionEvent | None
    file: str | None
    line: int | None
    function: str | None
    state: dict[str, object]
    call_stack: list[str]
    source: list[SourceLine]
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
                source=[],
                position=recorder.position,
                total_events=len(execution.events),
            )

        source_viewer = SourceViewer(event.file)

        return cls(
            event=event,
            file=source_viewer.file.as_posix(),
            line=event.line,
            function=event.function,
            state=recorder.state.snapshot(),
            call_stack=_build_call_stack(
                execution.events,
                recorder.position,
            ),
            source=source_viewer.get_context(event.line),
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
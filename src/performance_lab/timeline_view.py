from dataclasses import dataclass

from performance_lab.events import ExecutionEvent
from performance_lab.execution import Execution


@dataclass(frozen=True)
class TimelineEntry:
    """Represents a single event in the execution timeline."""

    position: int
    event_type: str
    function: str
    file: str
    line: int
    is_current: bool


@dataclass(frozen=True)
class TimelineView:
    """Represents the execution timeline for the digital microscope."""

    entries: list[TimelineEntry]
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
    def from_execution(cls, execution: Execution) -> "TimelineView":
        position = execution.recorder.position

        entries = [
            TimelineEntry(
                position=index,
                event_type=event.event_type.value,
                function=event.function,
                file=event.file,
                line=event.line,
                is_current=index == position,
            )
            for index, event in enumerate(execution.events)
        ]

        return cls(
            entries=entries,
            position=position,
            total_events=len(execution.events),
        )
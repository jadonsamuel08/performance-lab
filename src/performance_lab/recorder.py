from performance_lab.events import ExecutionEvent, EventType
from performance_lab.state import ProgramState
from performance_lab.timeline import Timeline


class Recorder:
    def __init__(self, events: list[ExecutionEvent]) -> None:
        self.timeline = Timeline(events)
        self.state = ProgramState()

    @property
    def events(self) -> list[ExecutionEvent]:
        return self.timeline.events

    @property
    def position(self) -> int:
        return self.timeline.position

    @property
    def current(self) -> ExecutionEvent | None:
        return self.timeline.current

    @property
    def finished(self) -> bool:
        return self.timeline.finished

    @property
    def started(self) -> bool:
        return self.timeline.started

    def step_forward(self) -> ExecutionEvent | None:
        event = self.timeline.step_forward()

        if event is not None:
            self.state.apply(event)

        return event

    def step_back(self) -> ExecutionEvent | None:
        event = self.timeline.step_back()

        if event is None:
            self.state = ProgramState()
            return None

        self._rebuild_state()

        return event

    def reset(self) -> None:
        self.timeline.reset()
        self.state = ProgramState()

    def _rebuild_state(self) -> None:
        self.state = ProgramState()

        for event in self.events[: self.position + 1]:
            self.state.apply(event)
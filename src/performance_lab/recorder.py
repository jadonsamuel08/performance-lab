from performance_lab.events import ExecutionEvent
from performance_lab.state import ProgramState


class Recorder:
    def __init__(self, events: list[ExecutionEvent]) -> None:
        self.events = events
        self.position = -1
        self.state = ProgramState()

    @property
    def current(self) -> ExecutionEvent | None:
        if self.position < 0 or self.position >= len(self.events):
            return None

        return self.events[self.position]

    @property
    def finished(self) -> bool:
        return self.position >= len(self.events) - 1

    @property
    def started(self) -> bool:
        return self.position >= 0

    @property
    def progress(self) -> float:
        if not self.events:
            return 0.0

        if self.position < 0:
            return 0.0

        return (self.position + 1) / len(self.events)

    def step_forward(self) -> ExecutionEvent | None:
        if self.finished:
            return self.current

        self.position += 1

        event = self.current

        if event is not None:
            self.state.apply(event)

        return event

    def step_back(self) -> ExecutionEvent | None:
        if self.position <= 0:
            self.reset()
            return None

        self.position -= 1

        self._rebuild_state()

        return self.current

    def jump_to(self, position: int) -> ExecutionEvent | None:
        if not self.events:
            self.reset()
            return None

        if position < 0:
            position = 0

        if position >= len(self.events):
            position = len(self.events) - 1

        self.position = position
        self._rebuild_state()

        return self.current

    def reset(self) -> None:
        self.position = -1
        self.state = ProgramState()

    def _rebuild_state(self) -> None:
        self.state = ProgramState()

        for event in self.events[: self.position + 1]:
            self.state.apply(event)
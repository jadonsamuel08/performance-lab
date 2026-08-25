from performance_lab.events import ExecutionEvent


class Recorder:
    def __init__(self, events: list[ExecutionEvent]) -> None:
        self.events = events
        self.position = -1

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

    def step_forward(self) -> ExecutionEvent | None:
        if self.finished:
            return self.current

        self.position += 1
        return self.current

    def step_back(self) -> ExecutionEvent | None:
        if self.position <= 0:
            self.position = -1
            return None

        self.position -= 1
        return self.current

    def reset(self) -> None:
        self.position = -1